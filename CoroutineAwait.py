
from collections import deque
import asyncio


STATUS_NEW = 'NEW'
STATUS_RUNNING = 'RUNNING'
STATUS_FINISHED = 'FINISHED'
STATUS_ERROR = 'ERROR'
STATUS_CANCELLED = "CANCELLED"


class Task:
    def __init__(self, coro):
        self.coro = coro  # Coroutine à exécuter
        self.name = coro.__name__
        self.status = STATUS_NEW  # Statut de la tâche
        self.return_value = None  # Valeur de retour de la coroutine
        self.error_value = None  # Exception levée par la coroutine

    # Exécute la tâche jusqu'à la prochaine pause
    def run(self):
        try:
            # On passe la tâche à l'état RUNNING et on l'exécute jusqu'à
            # la prochaine suspension de la coroutine.
            self.status = STATUS_RUNNING
            next(self.coro)
        except StopIteration as err:
            # Si la coroutine se termine, la tâche passe à l'état FINISHED
            # et on récupère sa valeur de retour.
            self.status = STATUS_FINISHED
            self.return_value = err.value
        except Exception as err:
            # Si une autre exception est levée durant l'exécution de la
            # coroutine, la tâche passe à l'état ERROR, et on récupère
            # l'exception pour laisser l'utilisateur la traiter.
            self.status = STATUS_ERROR
            self.error_value = err

    def is_done(self):
        return self.status in {STATUS_FINISHED, STATUS_ERROR}

    def __repr__(self):
        result = ''
        if self.is_done():
            result = " ({!r})".format(self.return_value or self.error_value)

        return "<Task '{}' [{}]{}>".format(self.name, self.status, result)

    def cancel(self):
        if self.is_done():
            # Inutile d'annuler une tâche déjà terminée
            return
        self.status = STATUS_CANCELLED

    def is_cancelled(self):
        return self.status == STATUS_CANCELLED

class Loop:
    def __init__(self):
        self._running = deque()

    def _loop(self):
        task = self._running.popleft()
        task.run()
        if task.is_done():
            print(task)
            return
        self.schedule(task)

    def run_until_empty(self):
        while self._running:
            self._loop()

    def schedule(self, task):
        if not isinstance(task, Task):
            task = Task(task)
        self._running.append(task)
        return task

    def run_until_complete(self, task):
        task = self.schedule(task)
        while not task.is_done():
            self._loop()

    def _loop(self):
        task = self._running.popleft()

        if task.is_cancelled():
            # Si la tâche a été annulée,
            # on ne l'exécute pas et on "l'oublie".
            print(task)
            return

DEFAULT_LOOP = Loop()

def cancel(task):
    # On annule la tâche
    task.cancel()
    # On laisse la main à la boucle événementielle pour qu'elle ait l'occasion
    # de prendre en compte l'annulation
    yield

def example():
    print("Tâche 'example'")
    print("Lancement de la tâche 'subtask'")
    sub = ensure_future(subtask())
    print("Retour dans 'example'")
    for _ in range(3):
        print("(example)")
        yield
    yield from cancel(sub)

def subtask():
    print("Tâche 'subtask'")
    for _ in range(2):
        print("(subtask)")
        yield


def ensure_future(coro, loop=None):
    if loop is None:
        loop = DEFAULT_LOOP
    return loop.schedule(coro)


event_loop = DEFAULT_LOOP
event_loop.run_until_complete(example())