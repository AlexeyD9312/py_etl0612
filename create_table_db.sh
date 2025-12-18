#!/bin/bash

# Переменные подключения
DB_CONTAINER_NAME=crypto_postgres    # имя контейнера Postgres
DB_USER=crypto_user
DB_NAME=crypto_db
DB_PORT=5434                           # порт на хосте

# Ждём, пока контейнер будет готов
echo "Waiting for Postgres container to be ready..."
sleep 5

# Список всех SQL-файлов по порядку
SQL_FILES=(
  "sql/create_tables/daily_prices.sql"
  "sql/create_tables/intraday_prices.sql"
  "sql/constraint_table/intraday_constraints.sql"
  "sql/constraint_table/daily_constraints.sql"
  "sql/indexes/intraday_indexes.sql"
  "sql/indexes/daily_indexes.sql"
)

# Применяем каждый файл к контейнеру
for FILE in "${SQL_FILES[@]}"; do
    echo "Applying $FILE ..."
    docker exec -i $DB_CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f /${FILE} 
done

echo "All tables, constraints, and indexes created successfully!"