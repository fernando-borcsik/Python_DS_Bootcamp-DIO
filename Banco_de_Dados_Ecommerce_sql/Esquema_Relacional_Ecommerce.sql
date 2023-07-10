-- -- Criação do banco de dados para o cenário de E-commerce
create database ecommerce;
use ecommerce;

-- Criar tabela cliente
create table clients(
	idClient int auto_increment primary key,
    Fname varchar(10),
    Minit varchar(3),
    Lname varchar(20),
    CPF char(11) not null,
    Address varchar(100),
    constraint unique_cpf_client unique (CPF)
);

alter table clients auto_increment=1;

-- Criar tabela produto
create table products(
	idProduct int auto_increment primary key,
    Pname varchar(30) not null,
    classification_kids bool default false,
    category enum('Eletrônico', 'Vestimenta', 'Brinquedos', 'Alimentos', 'Móveis') not null,
    size varchar(20),
    constraint unique_name_product unique (Pname)
);

alter table products auto_increment=1;

-- Criar tabela pedido
create table orders(
	idOrder int auto_increment primary key,
    idOrderClient int,
    orderStatus enum('Cancelado', 'Confirmado', 'Em processamento') default 'Em processamento',
    orderDescription varchar(255),
    deliveryPrice float default 10,
    paymentType enum('PIX', 'Boleto', 'Cartão') default 'Cartão',
    constraint fk_order_client foreign key (idOrderClient) references clients(idClient)
);

alter table orders auto_increment=1;

-- Criar tabela pagamento
create table payments(
	idPayment int auto_increment primary key,
    idOrderPayment int,
    statusPayment enum('Recusado', 'Pendente', 'Aprovado') default 'Pendente',
    constraint fk_payment_order foreign key (idOrderPayment) references orders(idOrder)
);

alter table payments auto_increment=1;

-- Criar tabela entregas
create table delivery(
	idDelivery int auto_increment primary key,
    idOrderDelivery int,
    trackCode varchar(100),
    deliveryStatus enum('Em processamento', 'Postado', 'A caminho', 'Entregue') default 'Em processamento',
    constraint fk_delivery_order foreign key (idOrderDelivery) references orders(idOrder)
);

alter table delivery auto_increment=1;

-- Criar tabela fornecedores
create table suppliers(
	idSupplier int auto_increment primary key,
    socialName varchar(40) not null,
    CNPJ char(15) not null,
    contact char(11) not null,
    constraint unique_supplier unique (CNPJ)
);

alter table suppliers auto_increment=1;

-- Criar tabela estoque
create table storages(
	idStorage int auto_increment primary key,
    idSupplier int,
    storageCity varchar(40),
    storageState char(2),
    constraint fk_supplier foreign key (idSupplier) references suppliers(idSupplier)
);

alter table storages auto_increment=1;

-- Criar tabela vendedores
create table sellers(
	idSeller int auto_increment primary key,
    socialName varchar(40) not null,
    abstName varchar(40),
    CNPJ char(15),
    CPF char(11),
    location varchar(40),
    contact char(11) not null,
    sellerEvaluation float,
    constraint unique_cnpj_seller unique (CNPJ),
    constraint unique_cpf_seller unique (CPF)
);

alter table sellers auto_increment=1;

-- Criar relacionamentos n:m
-- Vendedores e Produtos
create table productSellers(
	idProductSeller int,
    idProduct_ps int,
    productPrice float not null,
    productEvaluation float,
    productSellerQuantity int not null,
    primary key (idProductSeller, idProduct_ps),
    constraint fk_product_seller foreign key (idProductSeller) references sellers(idSeller),
    constraint fk_product_product foreign key (idProduct_ps) references products(idProduct)	
);

-- Pedidos e Produtos
create table productOrders(
	idProduct_po int,
    idOrder_po int,
    idSeller_po int,
    productOrderQuantity int default 1,
    primary key (idProduct_po, idOrder_po, idSeller_po),
    constraint fk_product_order foreign key (idOrder_po) references orders(idOrder),
    constraint fk_product_id foreign key (idProduct_po) references products(idProduct),
    constraint fk_product_seller_id foreign key (idSeller_po) references sellers(idSeller)
);

-- Estoques e Produtos
create table productStorages(
	idProduct_pst int,
    idStorage_pst int,
    productStoredQuantity int default 1,
    primary key (idProduct_pst, idStorage_pst),
    constraint fk_product_storage foreign key (idStorage_pst) references storages(idStorage),
    constraint fk_storage_product_id foreign key (idProduct_pst) references products(idProduct)
);

-- Fornecedores e Produtos
create table sellerSuppliers(
	idSeller_ss int,
    idSupplier_ss int,
    primary key (idSeller_ss, idSupplier_ss),
    constraint fk_seller_seller foreign key (idSeller_ss) references sellers(idSeller),
    constraint fk_seller_supplier foreign key (idSupplier_ss) references suppliers(idSupplier)
);


