from math import inf, ceil

def orientation(p,q,r):
	s=(q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1])
	return 0 if s==0else 1 if s>0 else -1

def slope(p1,p2):
	if p1[0]==p2[0]: return inf
	return (p2[1]-p1[1])/(p2[0]-p1[0])

def getMinX(P):
	min_p = P[0]
	i=0
	for point in range(len(P[1:])):
		if P[point][0] < min_p[0] or (P[point][0]==min_p[0] and P[point][1]<min_p[1]):
			min_p = P[point]
			i = point
	return (min_p, i)

def graham(p):
	if len(p)<4: return p
	P = p[:]
	# Find lowest point
	min_p,i=getMinX(P)
	P.pop(i)

	hull=[min_p]	

	# Sort points by slope of line (min_p,p) (so increasing cosine angle)
	P.sort(key=(lambda x: [slope(x,min_p), -x[1], x[0]]))

	# Take minimum angle point as also on the hull
	for point in P:
		while len(hull) > 1 and orientation(hull[-2], hull[-1], point)<0:
			hull.pop()
		hull.append(point)
		
		
	return hull 

def jarvis(p):
	if len(p)<4: return p
	P = p[:]
	# Find lowest point
	min_p = getMinX(P)[0]
			
	hull = []
	h=min_p
	i=0
	candidate = min_p
	while True:
		hull.append(h)
		h=P[0]
		for point in P:
			if h==hull[-1] or orientation(hull[-1], h, point) <0:
				h = point

		if h==hull[0]:
			break
	
	return hull


def getCandidateLinear(pt, P):
	# P is sorted in ccw order
	# so use binary search on angle to find candidate where all points are on other side of line

	if len(P) < 3:
		return P[0] if orientation(pt, P[0], P[1]) < 0 else P[1]
	
	for i in range(len(P)):
		l_n = P[(i-1)%len(P)]
		r_n = P[(i+1)%len(P)]
		if orientation(pt, P[i], l_n) >= 0 and orientation(pt, P[i], r_n) >= 0 and P[i] != pt:
			return P[i]
		

	return None

def getCandidateLog( p, hull):
	"""Return the point in hull that the right tangent line from p
	to hull touches.
 	Code based of code by Tom Switzer, see:  https://gist.github.com/tixxit/252229
	"""
	l, r = 0, len(hull)
	l_prev = orientation(p, hull[0], hull[-1])
	l_next = orientation(p, hull[0], hull[(l + 1) % r])
	while l < r:
		print(l,r)
		c = ceil((l + r) / 2)
		print(c)
		c_prev = orientation(p, hull[c], hull[(c - 1) % len(hull)])
		c_next = orientation(p, hull[c], hull[(c + 1) % len(hull)])
		c_side = orientation(p, hull[l], hull[c])
		if c_prev != 1 and c_next != 1:
			return hull[c]
		elif c_side == -1 and (l_next == 1 or
									  l_prev == l_next) or \
				c_side == 1 and c_prev == 1:
			r = c-1               # Tangent touches left chain
		else:
			l = c + 1           # Tangent touches right chain
			l_prev = -c_next    # Switch sides
			l_next = orientation(p, hull[l], hull[(l + 1) % len(hull)])
		print(l,r)
	return hull[l]


def chans(p):
	if len(p)<4: return p
	P=p[:]
	m = 2
	i=0
	min_p,i = getMinX(P)
	p_0 = (-inf, 0)
	while True:
		#phase 1
		k = ceil(n//m)
		groups = [points[i*m:(i+1)*m] for i in range(k)]
		hulls = [graham(g) for g in groups if len(g)>0]
		hull = []
		h = min_p
		for i in range(m):
			hull.append(h)
			pt = hull[-1]
			candidates = [getCandidateLinear(pt, g) for g in hulls]
			h = candidates[0]
			for cnd in candidates:
				if h==pt or orientation(pt,h,cnd) < 0:
					h = cnd

			if hull[0]==hull[-1] and len(hull)>1:
				return hull[0:len(hull)-1]
		i += 1
		m=min(len(P),2**(2**i))


		




if __name__=='__main__':
	import random
	from scipy import spatial	
	def randomPoint(xmin,xmax,ymin,ymax):
		return (random.randint(xmin,xmax), random.randint(ymin,ymax))

	def reportWrongPoint(algorithm, index, h,sh):
		print(f"{algorithm} disagrees with Scipy solution at index {i}, found {h}, should be {sh}.")
	def reportWrongLength(algorithm, l,sl):
		print(f">>> {algorithm} returns hull of wrong length {l}, should be {sl}")

	candidateTest = 0
	if candidateTest:
		print("Default Test of getCandidateLinear")
		testp = (1,8)
		testH = [(1, 8), (2, 3), (24, 14), (23, 22)]
		print(getCandidateLinear(testp, testH))
		import sys
		sys.exit(0)

	n=100
	points = [randomPoint(1,1000,1,1000) for _ in [0]*n]
	points=list(set(points))
	print(points)
	min_p,i = getMinX(points)
	h1=graham(points)
	print("Hull from Graham")
	print(h1)
	print()
	
	h2 = jarvis(points)
	print("Hull from Jarvis")
	print(h2)
	print()

	h3 = chans(points)
	print("Hull from Chans")
	print(h3)
	print()

	print("Hull from Scipy.spatial.ConvexHull")
	h4 = spatial.ConvexHull(points)
	scihull = [points[i] for i in h4.vertices]
	n = scihull.index(min_p)
	scihull = scihull[n:] + scihull[:n]
	print(scihull) 
	print()

	print("Results:")
	print("Checking lengths of returned hulls...")
	gl = len(h1)
	jl=len(h2)
	cl=len(h3)
	sl=len(h4.vertices)
	results = [("Graham",gl,h1),("Jarvis", jl, h2), ("Chan",cl,h3)]
	lFlag=False
	eFlag=False
	for result in results:
		if result[1] != sl:
			reportWrongLength(result[0], result[1], sl)
			lFlag=True
	if not lFlag:
		print(">>> All hulls are of the correct length! Checking elements...")
		for result in results:
			for i in range(len(result[2])):
				if result[2][i] != scihull[i]:
					reportWrongPoint(result[0], i, result[2],scihull)
					eFlag=True
		if not eFlag:
			print(">>> All tests have passed successfully!")




