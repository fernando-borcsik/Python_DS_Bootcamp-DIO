-- -- Inserção de dados em ecommerce
use ecommerce;

insert into clients (Fname, Minit, Lname, CPF, Address)
	values ('Maria', 'M', 'Silva', 12345678901, 'rua silva de prata 29, Carangola - Cidade das flores'),
			('Matheus', 'O', 'Pimentel', 98765432120, 'rua alameda 289, Centro - Cidade das flores'),
            ('Ricardo', 'F', 'Silva', 45678912378, 'avenida alameda vinha 1009, Centro - Cidade das flores'),
            ('Julia', 'S', 'França', 78912345633, 'rua laranjeiras 861, Centro - Cidade das flores'),
            ('Roberta', 'G', 'Assis', 98745632109, 'avenida koller 19, Centro - Cidade das flores'),
            ('Isabela', 'M', 'Cruz', 65478912308, 'rua alameda das flores 28, Centro - Cidade das flores');

insert into products (Pname, classification_kids, category, size)
	values ('Fone de ouvido', false, 'Eletrônico', null),
			('barbie Elsa', true, 'Brinquedos', null),
            ('Body Carters', true, 'Vestimenta', null),
            ('Microfone Vedo - Youtuber', false, 'Eletrônico', null),
            ('Sofá retrátil', false, 'Móveis', '3x57x80'),
            ('Farinha de arroz', false, 'Alimentos', null),
            ('Fire stick Amazon', false, 'Eletrônico', null);
            
insert into orders (idOrderClient, orderStatus, orderDescription, deliveryPrice, paymentType)
	values (1, default, 'compra via aplicativo', default, default),
			(2, default, 'compra via aplicativo', 50, 'PIX'),
            (3, 'Confirmado', null, default, default),
            (4, default, 'compra via web site', 150, 'Boleto'),
            (2, default, null, default, default);

insert into payments (idOrderPayment, statusPayment)
	values (1, default),
			(2, 'Aprovado'),
            (3, 'Aprovado'),
            (4, default),
            (5, default);
            
insert into delivery (idOrderDelivery, trackCode, deliveryStatus)
	values (1, 'BFBDfoirngnd8t968450385', 'Entregue'),
			(2, 'SBJHSBF884594869847643', 'A caminho'),
            (3, 'BXNCBV1651616516516516151', 'Entregue'),
            (4, 'CBBC5416516519865150', 'Postado'),
            (5, 'BBBCBNCN398564769875986', default);
            
insert into suppliers (socialName, CNPJ, contact)
	values ('Almeida e Filhos', 123456789123456, '12325665478'),
			('Eletrônicos Silva', 254455879632012, '22245687595'),
            ('Eletrônicos Valma', 555555698745554, '33323254568');

insert into storages (idSupplier, storageCity, storageState)
	values (1, 'Sorocaba', 'SP'),
			(1, 'Votorantim', 'SP'),
            (2, 'Belo Horizonte', 'MG'),
            (3, 'Fortaleza', 'CE'),
            (3, 'Cascavel', 'CE');

insert into sellers (socialName, abstName, CNPJ, CPF, location, contact, sellerEvaluation)
	values ('Tech electronics', null, 115151411816516, null, 'RJ', 22145212589, 4.8),
			('Botique Durgas', null, null, 65457548965, 'RS', 77845799548, 4.1),
            ('Kids World', null, 654213789428569, null, 'SP', 11235469875, 3.9);

-- Preenchendo relacionamentos
insert into productOrders (idProduct_po, idOrder_po, idSeller_po, productOrderQuantity)
	values (1, 1, 1, 2),
			(2, 1, 3, 1),
            (3, 2, 2, 1),
            (4, 2, 1, 2),
            (7, 3, 3, 2),
            (5, 4, 2, 1),
            (1, 4, 1, 1),
            (1, 5, 2, 2);

insert into productSellers (idProductSeller, idProduct_ps, productPrice, productEvaluation, productSellerQuantity)
	values (1, 1, 20, 4.5, 20),
			(1, 4, 100, 4.7, 50),
            (2, 1, 22.5, 4.4, 10),
            (2, 3, 54.9, 4.1, 30),
            (2, 5, 300, 3.8, 15),
            (2, 6, 10, 4.4, 100),
            (3, 2, 99.9, 4.9, 30),
            (3, 7, 22.8, 3.7, 20);

insert into sellerSuppliers(idSeller_ss, idSupplier_ss)
	values(1, 1),
			(1, 2),
            (2, 2),
            (2, 3),
            (3, 3);

insert into productStorages(idProduct_pst, idStorage_pst, productStoredQuantity)
	values (1, 1, 500),
			(1, 2, 400),
            (4, 2, 300),
            (4, 3, 100),
            (7, 5, 50),
            (5, 5, 100),
            (2, 4, 1000),
            (3, 4, 500),
            (5, 4, 50),
            (6, 4, 200);

