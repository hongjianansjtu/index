#include<pbc/pbc.h>
#include<unistd.h>
#include<sys/types.h>
#include<fcntl.h>
#include<sys/stat.h>

#include<time.h>
#define NUMBER 1000
class Accumulator{
	private:
		pairing_t pairing;
		element_t msk;
	public:
		element_t Delta, g, g2, pubkey;
		Accumulator();
		~Accumulator();
		void randomG1(element_t u);
		void randomZr(element_t u);
		void member_register(element_t A, element_t x);
		bool mappingcheck(element_t left1, element_t left2, element_t right1, element_t right2);
		bool membercheck(element_t A, element_t x);
};

struct User{
	element_t A;
	element_t x;
};

bool Accumulator::membercheck(element_t A, element_t x){
	element_t left, right1, right2, tmp;
	element_init_GT(left, pairing);
	element_init_GT(right1, pairing);
	element_init_GT(right2, pairing);
	element_init_G2(tmp, pairing);
	element_pow_zn(tmp, g2, x);
	pairing_apply(left, Delta, g2, pairing);
	pairing_apply(right1, A, tmp, pairing);
	pairing_apply(right2, A, pubkey, pairing);
	element_mul(right1, right1, right2);
	return !element_cmp(left,right1);
}

bool Accumulator::mappingcheck(element_t left1, element_t left2, element_t right1, element_t right2){
	element_t left, right;
	element_init_GT(left, pairing);
	element_init_GT(right, pairing);
	pairing_apply(left, left1, left2, pairing);
	pairing_apply(right, right1, right2, pairing);
	return !element_cmp(left, right);
}

Accumulator::Accumulator(){
	char param[4000];
	int fd = open("./d224.param", O_RDONLY);
	size_t count = read(fd, param, 4000);
	if(!count) pbc_die("input error");
	pairing_init_set_buf(pairing, param, count);
	printf("construct complete\n");
	element_init_G1(Delta, pairing);
	element_init_G1(g, pairing);
	element_init_G2(g2, pairing);
	element_init_G2(pubkey, pairing);
	element_init_Zr(msk, pairing);
	element_random(Delta);
	element_random(msk);
	element_random(g);
	element_random(g2);
	element_pow_zn(pubkey, g2, msk);
}

Accumulator::~Accumulator(){
	element_clear(Delta);
	element_clear(msk);
	element_clear(g2);
	element_clear(pubkey);
	printf("deleted\n");
}

void Accumulator::randomG1(element_t u){
	element_init_G1(u, pairing);
	element_random(u);
}

void Accumulator::randomZr(element_t u){
	element_init_Zr(u, pairing);
	element_random(u);
}

void Accumulator::member_register(element_t A, element_t x){
	element_t tmp1, one;
	element_init_Zr(tmp1, pairing);
	element_init_Zr(one, pairing);
	element_set1(one);
	element_add(tmp1, x, msk);
	element_div(tmp1, one, tmp1);
	element_pow_zn(A, Delta, tmp1);
	element_clear(tmp1);
	element_clear(one);
}

int main(){
	Accumulator*a = new Accumulator();
	struct User u[NUMBER];
	clock_t begin, end;

	for(int i = 0; i<NUMBER; i++){
		a->randomG1(u[i].A);
		a->randomZr(u[i].x);
	}
    begin = clock();
	for(int i = 0; i<NUMBER; i++){
		a->member_register(u[i].A, u[i].x);
	}
	end = clock();
	for(int i = 0; i < NUMBER; i++){
		element_clear(u[i].A);
		element_clear(u[i].x);
	}
	double during = (double)(end- begin)/CLOCKS_PER_SEC;
	//double during = (double)(end- begin);
	printf("Time: %f\n", during);
	delete a;
	return 0;
}
