// (!) by Giovanni Squillero <giovanni.squillero@polito.it>
// +---------------------------------------------------------+
// |   -=*=-  THIS FILE IS NOT INTENDED FOR SHARING  -=*=-   |
// +---------------------------------------------------------+
// The intellectual and technical concepts are proprietary.
// Reproduction or distribution is prohibited and may result
// in civil charges and criminal penalties.

void foo(void);

long int onemax(void)
{
    foo();
    return -1;
}

void foo(void)
{
    register long int x = -1;
}
