int main(){
    int sum = 0;
    int a = 10;
    int b = 30;
    int i;
    for (i = 0; i<100; i+10){
        sum = sum + (a*b) + i;
    }
    return sum;
}