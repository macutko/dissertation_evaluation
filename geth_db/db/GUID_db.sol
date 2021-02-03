pragma solidity ^0.5.16;

contract GUID_mapping {

    //    GUID => Subject => Grade
    mapping(string => mapping(string => string)) public grades;

    //    GUID => Subjects[]
    mapping(string => string[]) public subjects;

    // Subject => position in subjects plus one
    mapping(string => mapping(string => uint)) private subjectPositions;

    function add_grade(string memory _guid, string memory _subject, string memory _grade) public {
        grades[_guid][_subject] = _grade;
        //                this subject does not exist yet
        if (subjectPositions[_guid][_subject] < 1) {
            subjectPositions[_guid][_subject] = subjects[_guid].length + 1;
            subjects[_guid].push(_subject);
        }
    }

    function get_grade(string memory _guid, string memory _subject) view public returns (string memory) {
        return grades[_guid][_subject];
    }

    function get_studentSubject(string memory _guid, uint iterator) view public returns (string memory) {
        return subjects[_guid][iterator];
    }

    function get_studentSubjectAmount(string memory _guid) view public returns (uint){
        return subjects[_guid].length;
    }

}
