docker-compose -f stories_microservices_event_bus_service/docker-compose.yml up -d &&
docker-compose -f stories_microservices_auth_service/docker-compose.yml up -d &&
docker-compose -f stories_microservices_post_service/docker-compose.yml  up -d &&
docker-compose -f stories_microservices_subscribers_service/docker-compose.yml  up -d &&
docker-compose -f stories_microservices_mailing_service/docker-compose.yml  up -d
docker-compose -f api_getaway/docker-compose.yml up -d