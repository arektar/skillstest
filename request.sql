
/*
Предположим у вас в базе данных есть три таблицы
Products (ProdId,ProdName)
Category(CatId,CatName)
Prod_Cat(ProdId,CatId)
Тогда запрос для выбора всех пар «Имя продукта – Имя категории»,
при условии, что если у продукта нет категорий, то его имя все равно должно выводиться,
будет выглядеть следующим образом
 */



SELECT ProdName,CatName  FROM (Products Left JOIN Prod_Cat USING (ProdId)) Left JOIN Category USING (CatId);