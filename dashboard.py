import argparse
import logging
import daemon
import websocket
import json
import psycopg2

psql_connection = None
websockets = []

def start_new_listener(websocket_url):
    socket = websocket.WebSocketApp(websocket_url,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    socket.run_forever()
    websockets.append(socket)


def grab_new_nodes():
    pass # need some endpoint first with network map


def on_message(ws, message):
    msg = json.loads(message)
    event = msg["event"]
    event_info = msg["data"]["number"]
    timestamp = msg["data"]["subblocks"][0]["transactions"][0]["transaction"]["metadata"]["timestamp"]
    logging.debug(f'Event: {event} - Event Info: {event_info} - Timestamp: {timestamp}')

    cur = psql_connection.cursor()
    cur.execute('INSERT INTO events (id, node_vk, event, event_info, timestamp) VALUES (default, %s, %s, %s, to_timestamp(%s))', ("5b09493df6c18d17cc883ebce54fcb1f5afbd507533417fe32c006009a9c3c4a", event, event_info, timestamp))
    cur.close()


def on_error(ws, error):
    logging.debug(error)


def on_close(ws, close_status_code, close_msg):
    logging.debug("Websocket connection closed")


def on_open(ws):
    logging.debug("Opened new websocket connection")


def main():
    log = logging.getLogger("Node Aggregator")
    parser = argparse.ArgumentParser(description="Node Aggregator Commands")
    parser.add_argument(
        '-d', '--daemon', help='Starts the server that listens to events in daemon mode', action="store_true")
    args = parser.parse_args()

    global psql_connection 
    psql_connection = psycopg2.connect("dbname='dashboard_admin' user='dashboard' host='localhost' password='noods'")
    psql_connection.autocommit = True

    if args.daemon:
        with daemon.DaemonContext():
            main_loop()
    else:
        main_loop()


def main_loop():
    start_new_listener("wss://masternode-01.lamden.io")


if __name__ == '__main__':
    log = logging.getLogger("Tests")
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    main()
