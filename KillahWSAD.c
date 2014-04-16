#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <time.h>
#define N	10


int arena_init(int player[], int enemy[]);
short int arena(int player[], int enemy[], short int death);
int move (char arrow, int player[], int enemy[]);
void refresh();


char getch() {
        char buf = 0;
        struct termios old = {0};
        if (tcgetattr(0, &old) < 0)
                perror("tcsetattr()");
        old.c_lflag &= ~ICANON;
        old.c_lflag &= ~ECHO;
        old.c_cc[VMIN] = 1;
        old.c_cc[VTIME] = 0;
        if (tcsetattr(0, TCSANOW, &old) < 0)
                perror("tcsetattr ICANON");
        if (read(0, &buf, 1) < 0)
                perror ("read()");
        old.c_lflag |= ICANON;
        old.c_lflag |= ECHO;
        if (tcsetattr(0, TCSADRAIN, &old) < 0)
                perror ("tcsetattr ~ICANON");
        return (buf);
}


int main ()
{
	short int death=0;
	int player[2], enemy[2], i;
	char arrow, any;
	system ("clear");
	printf("\t\tEAT IT\t\t\n\n\t\tKurtz's\n\n");
	printf("\n You are the W and you have to eat the X.\n Ready?\n");
	sleep(1);
	printf("press Enter\n");
	scanf("%c", &any);
	refresh();
	arena_init(player, enemy);
	while (death!=1)
	{
		//scanf("%c", &arrow);
		arrow= getch();
		move (arrow, player, enemy);
		refresh();
		arena(player, enemy, death);
	}
	/*while (death!=1)
	{
		//qui è il giocchetto
	}*/
	return 0;
}


int arena_init(int player[2], int enemy[2])
{
	char ARENA[N][N];
	int i, j;
	player[0]=4;
	player[1]=4;
	enemy[0]=9;
	enemy[1]=9;


	printf("\n");
	for (i=0; i<N; i++)
	{
		for (j=0; j<N; j++)
		{
			if (player[0]==i && player[1]==j)
			{ 	ARENA[i][j] = 'W';	}
			else
			if (enemy[0]==i && enemy[1]==j)
			{	ARENA[i][j] = 'X';		}
			else
			{	ARENA[i][j] = 183;	}
		}
	}

	for (i=0; i<N; i++)
	{
		for (j=0; j<N; j++)
		{
			printf(" %c ", ARENA[i][j]);
		}
		printf("\n");

	}
	printf("\n");

	return player[2], enemy[2];
}

void refresh ()
{
	int i;
		for (i=0; i<(N+2); i++)
		{
			   fputs("\033[A\033[2K",stdout);
		}
		//fputs("\033[A\033[2K",stdout);
		rewind(stdout);
}

short int arena (int player[2], int enemy[2], short int death)
{
	int i, j;
	char ARENA[N][N];

	printf("\n");
	if (player[0]==enemy[0] && player[1]==enemy[1])
	{
		printf("\n\n\nYOU ATE THE MOTHEFUCKER!!!!\n\n\n");
		death= 1;
	}
	else
	{		for (i=0; i<N; i++)
			{
				for (j=0; j<N; j++)
				{
					if (player[0]==i && player[1]==j)
					{ 	ARENA[i][j] = 'W';	}
					else
					if (enemy[0]==i && enemy[1]==j)
					{	ARENA[i][j] = 'X';		}
					else
					{	ARENA[i][j] = 183;	}
				}
			}

			for (i=0; i<N; i++)
			{
				for (j=0; j<N; j++)
				{
					printf(" %c ", ARENA[i][j]);
				}
				printf("\n");

			}
	}

	return death;
}


int move (char arrow, int player[2], int enemy[2])
{
			if(arrow== 'w')
			{
				if ((player[0]-1)<0)
				{player[0]= N+(player[0]-1);}
				else
				{player[0]= player[0]-1;}
			}
			if(arrow== 's')
			{ player[0]=(player[0]+1)%N;}
			if(arrow== 'd')
			{ player[1]=(player[1]+1)%N;}
			if(arrow== 'a')
			{
				if ((player[1]-1)<0)
				{player[1]= N+(player[1]-1);}
				else
				{player[1]= player[1]-1;}
			}

					srand(time(NULL));
					float x,y;
					x=(float) rand()/(RAND_MAX);
					y=(float) rand()/(RAND_MAX);

					if(y > 0.5)
					{
						if(x<=0.5)
						{
							if ((enemy[0]-1)<0)
							{enemy[0]= N+(enemy[0]-1);}
							else
							{enemy[0]= enemy[0]-1;}

						}
						else
						{ enemy[0]=(enemy[0]+1)%N;}
					}
					else
					{
						if(x<=0.5)
						{

							if ((enemy[1]-1)<0)
							{enemy[1]= N+(enemy[1]-1);}
							else
							{enemy[1]= enemy[1]-1;}


						}
						else
						{ enemy[1]=(enemy[1]+1)%N;}
					}


	arrow='o';
	return arrow, player[2], enemy[2];
}
