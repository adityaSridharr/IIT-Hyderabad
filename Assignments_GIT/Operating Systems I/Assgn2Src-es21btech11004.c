#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

//This function checks if num is a perfect number
int ifPerf(int num) {
  int sumOfFact = 0;
  for (int i = 1; i < num; i++) {
    if (num % i == 0) {
      sumOfFact += i;
    }
  }
  if (sumOfFact == num) {
    return 1;
  } 
  else {
    return 0;
  }
}



/*The allocation is as follows : Let's say n = 100, k = 7.
Thread 1 - Checks {1, 8, 15,...., 99}
Thread 2 - Checks {2, 9, 16,...., 100}
Thread 3 - Checks {3, 10, 17,..., 91}
Thread 7 - Checks {7, 14, 21,..., 98}*/

void *threadAlloc_perfCheck(void *parameters) {
  
  int *par = (int *)parameters;
  int n = par[0];
  int k = par[1];
  int i = par[2];

  //File Handling of individual files for threads
  FILE *threadFile = NULL;
  char nameOfFile[20];
  sprintf(nameOfFile , "OutFile%d.txt" , i + 1);
  threadFile = fopen(nameOfFile, "w");

  //File Handling of the main file OutMain.txt
  FILE *mainFile = NULL;
  mainFile = fopen("OutMain.txt", "a");
  if(mainFile == NULL){
    printf("Alert! Unable to open the file...");
    exit(1);
  }

  int adder = i + 1;
  //This array stores all perfect numbers for that thread
  int isPerf[n / k];  
  int numOfPerf = 0;
  for (int j = 0; j <= n / k; j++) {
    int numToCheck = (j * k + adder);
    if (numToCheck <= n) {
      
      if (ifPerf(numToCheck) == 1) {
        isPerf[numOfPerf] = numToCheck;
        numOfPerf += 1;
        fprintf(threadFile, "%d : Is a perfect Number\n" , numToCheck);
      }
        
      else{
        fprintf(threadFile , "%d : Is not a perfect Number\n" , numToCheck);
      }
    }
  }

  //We append the perfect number details on to the main output file.
  fprintf(mainFile, "\nThread %d.", adder);
  for (int k = 0; k < numOfPerf; k++) {
    fprintf(mainFile, "%d ", isPerf[k]);
  }
  fclose(threadFile);
  fclose(mainFile);
  pthread_exit(0);
}



int main(int argc, char *argv[]) {
  int n, k;
  FILE *inputFile = NULL;
  inputFile = fopen(argv[1] , "r");
  if(inputFile == NULL){
      printf("Alert! Unable to open the file...");
      exit(1);
  }
  else{
      fscanf(inputFile , "%d %d" , &n , &k);
  }

  
  FILE *mainFile = NULL;
  mainFile = fopen("OutMain.txt", "a");
  if(mainFile == NULL){
    printf("Alert! Unable to open the file...");
    exit(1);
  }

  //Condition where we don't need all threads for the process.
  if (k > n){
    fprintf(mainFile, "Threads ");
    for (int i = n + 1; i <= k; i++){
      fprintf(mainFile, "%d, ", i);
    }
    fprintf(mainFile, "were not required to perform operations");
    k = n;
  }
  

  pthread_t tid[k];
  pthread_attr_t attr;
  pthread_attr_init(&attr);
  //We store n, k and i in a pointer variable and typecast to (void *) to create the thread.
  int *parameters = (int *)malloc(sizeof(int) * 3);
  parameters[0] = n;
  parameters[1] = k;

  for (int i = 0; i < k; i++) {
    parameters[2] = i;
    pthread_create(&tid[i], &attr, threadAlloc_perfCheck, (void *)parameters);
    pthread_join(tid[i], NULL);
  }
  free(parameters);
  fclose(inputFile);
}