# macabre_simplifile

Fork of [simplifile](https://github.com/bcpeinhardt/simplifile) (Apache-2.0) that ports the
entire library to [macabre](https://github.com/anomalyco/macabre)'s Python target. The public
API and all pure Gleam code are unchanged; only the Erlang/JavaScript FFI was replaced with
Python externals.

Because the module is still named `simplifile`, existing code keeps working with:

```gleam
import simplifile
```

## Example

```gleam
let filepath = "./test/hello.txt"
let assert Ok(_) = "Hello, World" |> simplifile.write(to: filepath)
let assert Ok(_) = "Goodbye, Mars" |> simplifile.append(to: filepath)
let assert Ok("Hello, WorldGoodbye, Mars") = simplifile.read(from: filepath)
let assert Ok(_) = simplifile.delete(filepath)
let assert Error(_) = simplifile.read(from: filepath)
```

## Installation

Add it to your macabre project (macabre resolves dependencies from git):

```sh
gleam add macabre_simplifile --git git@github.com:dusty-phillips/macabre_simplifile.git
```

`macabre_simplifile` depends on the `macabre_filepath` fork, so add that to your project too:

```sh
gleam add macabre_filepath --git git@github.com:dusty-phillips/macabre_filepath.git
```

Both packages must also be listed in your project's `gleam.toml` as git dependencies for
macabre to pick them up:

```toml
[dependencies]
macabre_filepath = { git = "git@github.com:dusty-phillips/macabre_filepath.git", ref = "main" }
macabre_simplifile = { git = "git@github.com:dusty-phillips/macabre_simplifile.git", ref = "main" }
```

## License

Apache-2.0, matching upstream simplifile.
