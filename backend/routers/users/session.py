from threading import Lock

class SessionStorage:
    session: dict[str, dict] = {} # TODO: Locking?
    lock = Lock()

    @staticmethod
    def set(session_id: str, key: str, value: any):
        SessionStorage.lock.acquire()
        if SessionStorage.session.get(session_id) is None:
            SessionStorage.session[session_id] = {}
        
        SessionStorage.session[session_id][key] = value
        SessionStorage.lock.release()

    @staticmethod
    def get(session_id: str, key: str) -> any | None:
        SessionStorage.lock.acquire()
        userSession = SessionStorage.session.get(session_id)
        result = None
        if userSession is not None:
            result = userSession[key]
        SessionStorage.lock.release()
        return result
    
    @staticmethod
    def clear(session_id: str):
        SessionStorage.lock.acquire()
        if SessionStorage.session.get(session_id):
            del SessionStorage.session[session_id]
        SessionStorage.lock.release()