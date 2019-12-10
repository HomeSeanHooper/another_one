from service import products_service
import logging

# Set up logger(s)
root_logger = logging.getLogger()
formatter = logging.Formatter(
    f"[%(levelname)s] %(name)s: %(message)s"
)
root_logger.info(
    "Starting up"
)

handler_for_docker_logs = logging.StreamHandler()
handler_for_docker_logs.setFormatter(formatter)
root_logger.addHandler(handler_for_docker_logs)

root_logger.setLevel(logging.INFO)


if __name__ == "__main__":
    reactor_args = {}

    def run_twisted_wsgi():
        from twisted.internet import reactor
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource

        pool = reactor.getThreadPool()

        resource = WSGIResource(reactor, pool, products_service.app)
        site = Site(resource)
        port = 8080
        reactor.listenTCP(port, site)
        reactor.run(**reactor_args)

    run_twisted_wsgi()
