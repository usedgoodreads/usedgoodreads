# How to contribute
:rocket: First off, **thank you** for your interest in contributing to usedgoodreads.com :+1:

We try our best to maintain an easy and hassle free deployment for usedgoodreads and any platform building on this repository. Therefore we would like to establish the following rules for contribution.

## Pull Requests

> *TL;DR:*
> - Pull requests against `master` are declined automatically if they are not comments or documentation.
> - All pull requests must be against `develop`.
> - All pull requests must rebase on current `master`.

There are two main branches: `develop` and `master`. The `develop` branch is being deployed as `staging` and is used for testing with real data from the production nodes. The `master` branch is the branch currently used as `production` (for details check #7).

`master`
1. No pull requests will be accepted if they are not comments or documentation or if the source is the `develop` branch.
2. All pull requests must based on the current HEAD of master -> A rebase is mandatory.
3. Travis CI/CD must run without problems (including unit and integration tests)

`develop`
1. Multiple `feature branch` merge/pull request are possible.
2. Rebase on master before opening a pull request (see above)
3. Travis CI/CD must run without problems (including unit and integration tests)

`feature branch`
1. All other branches are treated as `feature branch`.
2. Lifetime should be shorter than 2 weeks. If feature is not merged till then either the change is too big and it will be split to smaller chunks or development will be postponed.
