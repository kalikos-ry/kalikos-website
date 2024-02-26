# Development

1. Set up environment `divio app setup kalikos -s test`
2. Run the project `divio project up`
3. Run migrations `docker-compose run --rm web python manage.py migrate`

## Syncing media and db
`divio app pull media` and `divio app pull db` to pull media and db from the server