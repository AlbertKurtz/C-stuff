//returns the decimal number in binary form

#include <stdio.h>
#include<stdbool.h>
#include<math.h>

int main()
{	
	int a, i, backnumb=0;
	printf("insert a decimal number:  ");
	scanf("%d", &a);
	int l=ceil(log2(a));
	bool n[l];

	i=0;
	while (a!=0)
	{
		n[i]=a%2;
		a/=2;
		i++;
	}
	printf("binary:  ");
	for (i=l-1; i>=0; i--)
	{
		printf("%d", (int) n[i]);
		backnumb+= ((int)n[i])*pow(2,i);
	}
	
	//backnumb is a check
	printf("\noriginal number:  %d", backnumb);
	printf("\n");
	return 0;
}
