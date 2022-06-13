#include <stdio.h>

// Shows that if needs an else block, and both need to terminate abnormally before code after becomes unreachable.

int main(){
    // this should print the numbers: 0, 0, 1, 2, 3, 4, 5
        int i = 0;
	while(i < 10){
		printf("%d\n",i);
		if (i == 5){
			break;
		} else {
			i++;
		}
		i = 10; // This instructon should stay reachable
	}
	i = 0;
	while(i < 10){
		printf("%d\n",i);
		if (i == 5){
			break;
		} else {
			i++;
			continue;
		}
		i = 10; // This instructon should become unreachable
	}
	return 0;
}
