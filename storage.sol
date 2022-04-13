// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract Storage {
    uint256 public myNumber;
    // bool myBool = true;
    // string myString = "Hey Beau";
    // int256 myInt = -3;
    // address myAddress = '';
    // bytes32 myBytes = 'squirell';

    struct People {
        uint256 id;
        string name;
    }

    People[] public person;

    mapping(uint256 => string) public idToName;

    function store(uint256 _myNumber) public {
        myNumber = _myNumber;
    }

    function retrieve() public view returns(uint256) {
        return myNumber;
    }

    function addPerson(string memory _name, uint256 _id) public {
        person.push(People({id:_id,name: _name}));
        idToName[_id] = _name;
    }

}