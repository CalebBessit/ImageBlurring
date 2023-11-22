//#include <CL/cl.h>
#define pi 3.141592653

__kernel void sum(__global const float *xs,__global  float *ys,  float t)
{
  int i = get_global_id(0);
  float x = xs[i];
  
  float g = -1;
  float disp = g/2 * (x*x - x) ;

  float An = 0;
  float Bn = 0;

  for(int n = 1; n<2000; n++)
  {
    if(n%2==1)
    {
      Bn = ( 4*g) / (n*n*n*pi*pi*pi);
      An = 2/(n*pi) * sin(n*pi/2);
    }
    else
    {
      An = 0;
      Bn = 0;
    }

    disp += An*sin(n*pi*x)*sin(n*pi*t) + Bn*sin(n*pi*x)*cos(n*pi*t);
  }
ys[i] =  disp;
/*
float disp = 0;
  for(int n=1; n < 50; n++)
  {
    float npi = n*pi;
    disp += ( 1/(npi*npi) )*cos(npi*t/2)*sin(npi*x/2) * ( 8*sin(npi/2) );
    
  }
  ys[i] =  disp;//sin(t + xs[i]); 
*/



}