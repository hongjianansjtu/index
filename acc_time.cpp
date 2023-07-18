#include<pbc/pbc.h>
#include<unistd.h>
#include<sys/types.h>
#include<fcntl.h>
#include<sys/stat.h>
#include<time.h>

#define NUMBER 1000
int main(){
 pairing_t pairing;
 char param[4000];
 int fd = open("./d224.param", O_RDONLY);
 size_t count = read(fd, param, 4000);
 if(!count) pbc_die("input error");
 pairing_init_set_buf(pairing, param, count);
 element_t g1,g2,x, gt;
 element_init_G1(g1, pairing);
 element_init_G2(g2, pairing);
 element_init_GT(gt, pairing);
 element_init_Zr(x, pairing);
 element_random(g1);
 element_random(g2);
 element_random(x);


 clock_t begin, end;
 begin = clock();
 for(int i = 0; i<NUMBER; i++){
	 element_pow_zn(g1, g1, x);
	 pairing_apply(gt, g1, g2, pairing);
 }

 end=clock();
 printf("%f\n", (double)(end-begin)/CLOCKS_PER_SEC);
 
 element_clear(g1);
 element_clear(g2);
 element_clear(gt);
 element_clear(x);
}
