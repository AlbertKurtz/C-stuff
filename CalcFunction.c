/* This Program calculate in terminal function inserted with the math.h syntax*/



#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main ()
{	
	FILE *coso;
	coso = fopen("coso.c", "w");
	
	double x, y;
	char form[100];

	printf("Insert Function\n");
	scanf("%s", form);
	//y= sin (x);

	fprintf (coso, "#include <stdio.h>\n#include <stdlib.h>\n#include <math.h>\nint main ()\n{\n	double x, y;\n	y=%s;\nprintf(\"%s=%%lf\\n\", y);\n	return 0;\n}\n", form, form);
	fclose (coso);
	system("/usr/bin/gcc coso.c -lm && ./a.out");
	return 0;
}
