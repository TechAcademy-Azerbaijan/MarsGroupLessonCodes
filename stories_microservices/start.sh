docker-compose -f stories_microservices_event_bus_service/docker-compose.yml up -d &&
docker-compose -f stories_microservices_auth_service/docker-compose.yml up -d &&
docker-compose -f stories_microservices_post_service/docker-compose.yml  up -d &&
docker-compose -f stories_microservices_subscribers_service/docker-compose.yml  up -d &&
docker-compose -f stories_microservices_mailing_service/docker-compose.yml  up -d
docker-compose -f deploy/docker-compose.yml up -d


#api/v1.0/comments/
#api/v1.0/auth/register
#api/v1.0/post/
#api/v1.0/subsribers/
#
#API Gateway