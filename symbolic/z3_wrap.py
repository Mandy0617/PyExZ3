# Copyright: see copyright.txt

import random
import sys
import ast
import logging

from z3 import *
from .z3_expr.integer import Z3Integer
from .z3_expr.bitvector import Z3BitVector

log = logging.getLogger("se.z3")


class Z3Wrapper(object):
	def __init__(self):
		self.N = 32
		self.asserts = None
		self.query = None
		self.use_lia = True
		self.z3_expr = None

		self.explore_repeat = 1

		# self.solver = Solver()

		# self.found_models = []
		self.solvers_list = []
		self.assertions_list = []
		self.additional_models = []
		# self.solver.set_option("smt.arith.random_initial_value", True)

	def createInput(self, solver,explore_repeat):
		if solver.check() == sat:
			# m = solver.model()
			ass = solver.assertions()
			# print(f"new_solver model: {m}")
			# print(f"new_solver ass: {ass}")
			new_solver = Solver()

			new_solver.add(ass)
			for i in range(0, explore_repeat):
				res = {}
				# print(f"new 2 solver asserts: {new_solver.assertions()}")

				if new_solver.check() == sat:
					m_new = new_solver.model()
					# print(f"new 2 solver model {i}: {new_solver.model()}")
					for var in m_new:
						new_solver.assert_exprs(var() != m_new[var()])

					for name in self.z3_expr.z3_vars.keys():
						try:
							ce = m_new.eval(self.z3_expr.z3_vars[name])
							res[name] = ce.as_signed_long()
						except:
							pass
					self.additional_models.append(res)


	def findCounterexample(self, asserts, query, explore_repeat):
		"""Tries to find a counterexample to the query while
	  	 asserts remains valid."""
		self.solver = Solver()
		self.explore_repeat = explore_repeat
		
		self.query = query
		self.asserts = self._coneOfInfluence(asserts,query)

		res = self._findModel()		
		
		log.debug("Query -- %s" % self.query)
		log.debug("Asserts -- %s" % asserts)
		log.debug("Cone -- %s" % self.asserts)
		log.debug("Result -- %s" % res)
		return res, self.additional_models #self.assertions_list

	# private

	# this is very inefficient
	def _coneOfInfluence(self,asserts,query):
		cone = []
		cone_vars = set(query.getVars())
		ws = [ a for a in asserts if len(set(a.getVars()) & cone_vars) > 0 ]
		remaining = [ a for a in asserts if a not in ws ]
		while len(ws) > 0:
			a = ws.pop()
			a_vars = set(a.getVars())
			cone_vars = cone_vars.union(a_vars)
			cone.append(a)
			new_ws = [ a for a in remaining if len(set(a.getVars()) & cone_vars) > 0 ]
			remaining = [ a for a in remaining if a not in new_ws ]
			ws = ws + new_ws
		return cone

	def _findModel(self):
		# Try QF_LIA first (as it may fairly easily recognize unsat instances)
		if self.use_lia:
			self.solver.push()
			self.z3_expr = Z3Integer()
			self.z3_expr.toZ3(self.solver,self.asserts,self.query)

			self.createInput(self.solver, self.explore_repeat)

			res = self.solver.check()
			self.solver.pop()
			if res == unsat:
				return None

		# now, go for SAT with bounds
		self.N = 32
		self.bound = (1 << 4) - 1
		while self.N <= 64:
			self.solver.push()
			(ret,mismatch) = self._findModel2()
			if (not mismatch):
				break

			self.solver.pop()
			self.N = self.N+8
			if self.N <= 64: print("expanded bit width to "+str(self.N)) 

		if ret == unsat:
			res = None
		elif ret == unknown:
			res = None
		elif not mismatch:
			self.createInput(self.solver, self.explore_repeat)

			res = self._getModel()
		else:
			res = None
		if self.N<=64: self.solver.pop()
		return res

	def _setAssertsQuery(self):
		self.z3_expr = Z3BitVector(self.N)
		self.z3_expr.toZ3(self.solver,self.asserts,self.query)

	def _findModel2(self):
		self._setAssertsQuery()
		int_vars = self.z3_expr.getIntVars()
		res = unsat
		while res == unsat and self.bound <= (1 << (self.N-1))-1:
			self.solver.push()
			constraints = self._boundIntegers(int_vars,self.bound)
			self.solver.assert_exprs(constraints)
			res = self.solver.check()

			if res == unsat:
				self.bound = (self.bound << 1)+1
				self.solver.pop()
		if res == sat:
			# Does concolic agree with Z3? If not, it may be due to overflow

			model = self._getModel()

			#print("Match?")
			#print(self.solver.assertions)
			self.solver.pop()
			mismatch = False
			for a in self.asserts:
				eval = self.z3_expr.predToZ3(a,self.solver,model)
				if (not eval):
					mismatch = True
					break
			if (not mismatch):
				mismatch = not (not self.z3_expr.predToZ3(self.query,self.solver,model))
			#print(mismatch)
			return (res,mismatch)
		elif res == unknown:
			self.solver.pop()
		return (res,False)

	def _getModel(self):
		
		res = {}
		model = self.solver.model()

		for name in self.z3_expr.z3_vars.keys():
			try:
				ce = model.eval(self.z3_expr.z3_vars[name])
				res[name] = ce.as_signed_long()
			except:
				pass
		return res
	
	def _boundIntegers(self,vars,val):
		bval = BitVecVal(val,self.N,self.solver.ctx)
		bval_neg = BitVecVal(-val-1,self.N,self.solver.ctx)
		return And([ v <= bval for v in vars]+[ bval_neg <= v for v in vars])

