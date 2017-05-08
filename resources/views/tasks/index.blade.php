<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>taks index</title>
  </head>
  <body>
    <ul>
      @foreach($tasks as $task)
      <li>
        <a href="tasks/{{ $task->id }}">
          #{{ $task->id }}:
        </a>
        {{ $task->body }}
      </li>
      @endforeach
    </ul>
  </body>
</html>