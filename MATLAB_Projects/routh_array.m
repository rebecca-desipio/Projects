clear all; close all; clc; syms x;
% User input
%p = [1 1 5 2 4]; % enter the coefficients of the polynomial
p = [1 1 2 2];

% defining variables
order = length(p);
array = sym(zeros(order,(order-2)));
p_even = p(1:2:order);
p_odd = p(2:2:order);
b = sym(ones(2,2));

% Setting up the Routh)-Array
for ii=1:length(p_even) %Sets the first row of the routh array
    array(1,ii) = p_even(ii);
end

for kk=1:length(p_odd) %Sets the second row of the routh array
    array(2,kk) = p_odd(kk);
end

count = 0;
next_row = 0;
for zz=3:length(p)
    for aa=1:order-2
        for jj=1:2
            b(jj,1) = array(jj+next_row,zz-2-next_row);
        end
        for kk=1:2
            b(kk,2) = array(kk+next_row,zz-1+count-next_row);
        end
        determinant = -1/(array((zz-1),1))*((b(4)*b(1)-b(2)*b(3)));
        if aa==1 && determinant(1,1) == 0
            array(zz,aa) = x;
            count = count+1;
        else
            array(zz,aa) = determinant;
            count = count+1;
        end
        if count==order-3
            count = 0;
            next_row = next_row+1;
            break
        end
    end
end

array

% Account for auxillary equations

  



