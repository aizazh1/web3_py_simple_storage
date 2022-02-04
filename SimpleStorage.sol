// SPDX-License-Identifier: MIT
// add license identifier to top of code to show that code is open source and establish trust

// version of solidity to use, required
pragma solidity ^0.6.0;

contract SimpleStorage {
    //this gets initialized to 0
    uint256 favoriteNumber;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public peopleArray;

    //mapping string to uint -> for people array
    mapping(string => uint256) public nameToFavoriteNumber;

    //public: can be accessed by anyone and is not transactional
    //internal: can only be inherited by internal elements but not accessed by external elements
    //private: can't be inherited by internal elements or accessed by external elements
    //external: can't be inherited by internal elements, but can only be accessed by external elements
    People public person = People({favoriteNumber: 2, name: "Aizaz"});

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    //view: only to view state, pure: only do maths, doesn't even read state
    //both are not transactional
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function retrieve2(uint256 _favoriteNumber) public pure returns (uint256) {
        return _favoriteNumber * 2;
    }

    //memory: only stored during execution of the function
    //storage: data will persist even after execution
    //string is an array of bytes. Since it is then an object, we need to decide where to store it
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        peopleArray.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
