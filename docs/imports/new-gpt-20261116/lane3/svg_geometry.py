"""Clip map rings to visible view; simplify to at most 0.25 native-pixel perpendicular error."""
def compact_ring(points,bounds=(20.,20.,620.,620.),tolerance=.25):
 pts=list(points)
 if len(pts)>1 and pts[0]==pts[-1]:pts.pop()
 left,top,right,bottom=bounds
 for axis,edge,keep_greater in [(0,left,True),(0,right,False),(1,top,True),(1,bottom,False)]:
  if not pts:return []
  out=[];a=pts[-1];ain=(a[axis]>=edge if keep_greater else a[axis]<=edge)
  for b in pts:
   bin=(b[axis]>=edge if keep_greater else b[axis]<=edge)
   if ain!=bin:
    t=(edge-a[axis])/(b[axis]-a[axis]);q=(a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]));out.append(q)
   if bin:out.append(b)
   a,ain=b,bin
  pts=out
 if len(pts)<3:return []
 pts.append(pts[0]);keep={0,len(pts)-1};stack=[(0,len(pts)-1)];tol2=tolerance*tolerance
 while stack:
  i,j=stack.pop();a,b=pts[i],pts[j];dx,dy=b[0]-a[0],b[1]-a[1];norm=dx*dx+dy*dy;maximum=-1;chosen=None
  for k in range(i+1,j):
   px,py=pts[k];t=max(0.,min(1.,((px-a[0])*dx+(py-a[1])*dy)/norm)) if norm else 0.
   dd=(px-a[0]-t*dx)**2+(py-a[1]-t*dy)**2
   if dd>maximum:maximum=dd;chosen=k
  if maximum>tol2:
   keep.add(chosen);stack.append((i,chosen));stack.append((chosen,j))
 result=[pts[i] for i in sorted(keep)]
 return result if len(result)>=4 else []
