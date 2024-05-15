# CryptoVerification and version tag generation service

This service allows to download some contracts (I found just 4 contracts that could be parsed, one of them even
satisfies ERC20)
Then user can get list of contract addresses that exist in the database.
After that you can try to get version's tag, if contract's source code implements main methods of ERC20 protocol
The tag would be stored in the database and user will gain it. Else source code doesn't satisfy ERC20 protocol user will
get none as a response.

## version's tag

I couldn't find the exact information about this tag, so I decided to create it by myself if the contract is valid. It
collects all methods and properties, turns into a string and then it hashes.
And it is as a unique version for each contract and if it changes even to a one symbol, the hash would be another
completely

## Prerequisites

* [Docker Installation](https://docs.docker.com/install/)
* [Docker Compose Installation](https://docs.docker.com/compose/install/)

## Development

* `make up` to build and run app and database
* `make down` to stop container
* `make remove` to remove image
* `make help` for help

## Endpoint

* http://0.0.0.0:8000/docs lists service's endpoints
* http://0.0.0.0:8000/v1/contract/contract to fill the database by contracts, which addresses were determined by system
  and which are valid.

> In future will be available to add contract by user, indicating address as a query parameter

* http://0.0.0.0:8000/v1/contract/contract-addresses to get a list of contracts' addresses
* http://0.0.0.0:8000/v1/contract/check_contract check if contract is valid and create a tag of version if it is valid. 

