clear all; close all; clc; syms x kp ki;
% User input
%p = [1 2 8 12 20 16 16]; % enter the coefficients of the polynomial
% p = [1 2 2 4 11 10];
p = [4 -.04*x 0.8*x];

% defining variables
order = length(p);
array = sym(zeros(order,(order-2)));
%array = zeros(order,(order-2));
p_even = p(1:2:order);
p_odd = p(2:2:order);
b = sym(ones(2,2));
%b = ones(2,2);
mat = []; 

% Setting up the Routh)-Array
for ii=1:length(p_even) %Sets the first row of the routh array
    array(1,ii) = p_even(ii);
end

for kk=1:length(p_odd) %Sets the second row of the routh array
    array(2,kk) = p_odd(kk);
end

        row_of_zero = all(array == 0,2);
        if  row_of_zero(2) == 1
            aux_order = length(p) -  find(row_of_zero,1);
            aux_poly = array(1,:);
            aux_poly_deriv = reshape([aux_poly; zeros(size(aux_poly))],[],1);
            aux_poly_deriv(end) = [];
            aux_poly_deriv = aux_poly_deriv';
            for rr=1:length(aux_poly_deriv)
                mat(rr) = double(aux_poly_deriv(rr));
            end
            co_eff_replace = polyder(mat);
            new_mat = sym(co_eff_replace);
            %co_new = co_eff_replace(1:2:length(co_eff_replace));
            if order == 3
               array(2,:) = new_mat(1,(1:order-1));
            else
               array(2,(1:length(new_mat(1,(1:2:order-2))))) = new_mat(1,(1:2:order-2));
            end
            
        end

count = 0;
next_row = 0;
new_co = [];
for zz=3:length(p) % iterates rows
    mat = [];

    for aa=1:order-2 % iterates columns
        for jj=1:2
            b(jj,1) = array(jj+next_row,zz-2-next_row);
        end
        for kk=1:2
            b(kk,2) = array(kk+next_row,zz-1+count-next_row);
        end
        
% 
        determinant = -1/(array((zz-1),1))*((b(4)*b(1)-b(2)*b(3)));
        if (aa<length(find(array(zz-1,:))) || aa<2) && determinant(1,1) == 0
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
    aux_row = [];
    for gg=1:order-2
        if isequal(array(zz,gg),x)
            aux_row(gg) = 0;
        else
            if has(array(zz,gg),x)
                disp("has an x")
                aux_row(gg) = 2;
            elseif isequal(double(array(zz,gg)),0)
                aux_row(gg) = 0;
            else
                aux_row(gg) = 2;
                disp("not a zero or x")
            end
        end
    end

    if all(aux_row==0,2)
        %isequal(array(zz),x) && all(array(zz,(length(find(array(zz-1,:))):end)) == 0,2)
        %if (zz-1) == find(row_of_zero,1)
        row_of_zero = all(array == 0,2);
            aux_order = find(row_of_zero,1) - 2;
            aux_poly = array(aux_order,:);
            for set_aux=1:length(aux_poly)
                if aux_poly(end) == 0
                    aux_poly(end) = [];
                end
            end
            aux_poly_deriv = reshape([aux_poly; zeros(size(aux_poly))],[],1);
            aux_poly_deriv(end) = [];
            aux_poly_deriv = aux_poly_deriv';
            for rr=1:length(aux_poly_deriv)
                mat(rr) = double(aux_poly_deriv(rr));
            end
            co_eff_replace = polyder(mat);
            index = 1;
            final_index = 1;
            mat_up = [];
            zeros_to_remove = [];
            zeros_to_remove = co_eff_replace==0;
            for pp=1:length(zeros_to_remove)
                if zeros_to_remove(pp) == 0
                    mat_up(index) = pp;
                    index = index+1;
                end
            end
            for yy=1:length(mat_up)
                final_mat(final_index) = co_eff_replace(mat_up(yy));
                final_index = final_index + 1;
            end
            new_mat = sym(final_mat);
            array(zz,(1:length(final_mat))) = new_mat;

        %end

    elseif zz == 3
        disp("do nothing");
    else
        row_of_zero = all(array == 0,2);
        if (zz-1) == find(row_of_zero,1)
            aux_order = length(p) -  find(row_of_zero,1) + 1;
            aux_poly = array(aux_order,:);
            aux_poly_deriv = reshape([aux_poly; zeros(size(aux_poly))],[],1);
            aux_poly_deriv(end) = [];
            aux_poly_deriv = aux_poly_deriv';
            for rr=1:length(aux_poly_deriv)
                mat(rr) = double(aux_poly_deriv(rr));
            end
            co_eff_replace = polyder(mat);
            
                     index = 1;
            final_index = 1;
            mat_up = [];
            zeros_to_remove = [];
            zeros_to_remove = co_eff_replace==0;
            for pp=1:length(zeros_to_remove)
                if zeros_to_remove(pp) == 0
                    mat_up(index) = pp;
                    index = index+1;
                end
            end
            for yy=1:length(mat_up)
                final_mat(final_index) = co_eff_replace(mat_up(yy));
                final_index = final_index + 1;
            end
            new_mat = sym(final_mat);
            array(zz,(1:length(final_mat))) = new_mat;
%             new_mat = sym(co_eff_replace);
%             %co_new = co_eff_replace(1:2:length(co_eff_replace));
% 
%             %array(zz-1,:) = new_mat(1,(1:order-2));
%             array(zz,(1:length(new_mat(1,(1:2:order-2))))) = new_mat(1,(1:2:order-2))
%             %co_new = co_eff_replace(1:2:length(co_eff_replace));
       end
    end


end

array


% Account for auxillary equations
% find a row of all zeros >> row_of_zero = all(array == 0,2)
% >> find(row_of_zero,1) >> gives me the row index which has all zeros
% polyder takes the derivative of a polynomial >> new_co = polyder(aux_eqn)
% insert zeros every other index >> new2 = reshape([a'; zeros(size(a'))],[],1);
% aux_order = length(p) -  find(row_of_zero,1) + 1


