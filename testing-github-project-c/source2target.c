/*
 *  source2target.c
 *  Created on: 31.12.2017
 *  Released: 01.01.2018
 *  Author: Sergey Lukyanchikov
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
	FILE *source=NULL, *target=NULL;
	char buff[1024];

	source=fopen("source.csv", "r");
	target=fopen("target.csv", "w");

	int fin=0;

	while(!fin)
	{
	  if(fgets(buff, 1024, source)==NULL)
	  {
	    break;
	  }
	  fprintf(target, buff);
	}

	printf("Operation completed.\n");
	fclose(target);
	fclose(source);

	return 0;
}
