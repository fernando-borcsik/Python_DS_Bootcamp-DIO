use ecommerce;

SELECT * FROM clients;
SELECT * FROM orders;
SELECT * FROM payments;

SELECT concat(Fname, ' ', Lname) as Name, CPF, orderStatus, paymentType, statusPayment 
FROM clients c, orders o, payments p 
WHERE c.idClient = o.idOrderClient 
AND o.idOrder = p.idOrderPayment
ORDER BY Name;

SELECT concat(Fname, ' ', Lname) as Name, CPF, orderStatus, paymentType, statusPayment FROM clients 
JOIN orders ON idClient = idOrderClient
JOIN payments ON idOrder = idOrderPayment
ORDER BY Name;

-- Capturando o valor total dos produtos, pra cada produto, pra cada pedido
CREATE TABLE total_price_product AS
SELECT idOrder_po, productOrderQuantity, productPrice, round(productOrderQuantity * productPrice, 2) as Total_price_product FROM productOrders po
JOIN productSellers ps ON po.idProduct_po = ps.idProduct_ps;

SELECT * FROM total_price_product;

-- Capturando o valor total de cada pedido
CREATE TABLE total_price_order
SELECT idOrder_po, sum(Total_price_product) as Total_price_products
FROM total_price_join
GROUP BY idOrder_po
ORDER BY idOrder_po;

SELECT * FROM total_price_order;

-- Capturando o custo total de cada pedido, incluindo o frete
SELECT idOrder, (Total_price_products + deliveryPrice) as Total_cost FROM orders
JOIN total_price_order ON idOrder = idOrder_po;

-- Verificando quantos pedidos cada cliente realizou
SELECT idClient, concat(FName, ' ', LName) as Name, COUNT(idOrder) as Orders
FROM clients LEFT OUTER JOIN orders ON idClient = idOrderClient
GROUP BY idClient
ORDER BY Name;

-- Verificando quais e quantos produtos cada fornecedor possui, em cada estoque
SELECT socialName as Supplier, Pname as Product, idStorage, storageState as State, storageCity as City, productStoredQuantity as Quantity FROM products 
JOIN productStorages ON idProduct = idProduct_pst
JOIN storages ON idStorage = idStorage_pst
JOIN suppliers ON storages.idSupplier = suppliers.idSupplier;

-- Verificando quais e quantos produtos cada fornecedor possui, no total
SELECT socialName as Supplier, Pname as Product, SUM(productStoredQuantity) as Quantity FROM products 
JOIN productStorages ON idProduct = idProduct_pst
JOIN storages ON idStorage = idStorage_pst
JOIN suppliers ON storages.idSupplier = suppliers.idSupplier
GROUP BY Supplier, Product;



