let chatify = angular.module('chatify', [], ($interpolateProvider) => {
     $interpolateProvider.startSymbol('[[');
     $interpolateProvider.endSymbol(']]');
});

chatify.controller('main', ['$scope', '$http', ($scope, $http) => {
    $scope.chatInputValue = null;
    $scope.chatInputFocus = false;
    $scope.searchInputValue = null;
    $scope.search = false;

    $scope.people = {
        message: null,
        data: []
    };

    $scope.toggleSearch = () => {
        $scope.search = !$scope.search;
    };

    $scope.searchInputHandler = () => {
        // TODO(0) something
    };

    $scope.onSearchChange = () => {
        $http.get("http://localhost:8000/chatify?search=" + $scope.searchInputValue).then((response) => {
            $scope.people = response.data;
        }, (response) => {
            $scope.message = response.data;
        });
    };

    $scope.chatFocusIn = () => {
        $scope.chatInputFocus = true;
    };

    $scope.chatFocusOut = () => {
        $scope.chatInputFocus = false;
    };

    document.addEventListener("keypress", (event) => {
        let key = event.which || event.keyCode;

        if(key === 13 && $scope.chatInputFocus && $scope.chatInputValue && $scope.chatInputValue.length > 0) {
            // TODO(1) do something with the input
            $scope.chatInputValue = "";
            $scope.$apply();

            event.preventDefault();
        }
    });
}]);

class Application {

    constructor() {
        // create WebSocket connection.
        this.socket = new WebSocket('ws://localhost:8000/socket');

        this.open();
        this.listen();
    }

    open() {
        console.log("Trying to connect");

        this.socket.addEventListener("open", event => {
            this.socket.send("Hello Server!");

            setTimeout(() => {
                this.socket.send("Once again it's me");
            }, 10000);
        });
    }

    listen() {
        this.socket.addEventListener('message', function (event) {
            console.log('Message from server ', event.data);
        });
    }
}

// let application = new Application();