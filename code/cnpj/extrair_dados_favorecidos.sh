pg_dump -h localhost -p 5432 -U postgres -W --table="favorecidos" --data-only --column-inserts sa > dados_favorecidos.sql
