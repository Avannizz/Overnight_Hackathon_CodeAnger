// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MediaRegistry {

    event MediaStored(address indexed uploader, string sha256Hash);

    struct Entry {
        address uploader;
        string sha256Hash;
        string pHash;
        string aiHash; // compact hash instead of full fingerprint
    }

    Entry[] public entries;

    function storeMedia(
        string memory sha256Hash,
        string memory pHash,
        string memory aiHash
    ) public {
        entries.push(Entry(msg.sender, sha256Hash, pHash, aiHash));
        emit MediaStored(msg.sender, sha256Hash);
    }

    function getTotal() public view returns (uint) {
        return entries.length;
    }
}
