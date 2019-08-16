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

    $scope.chatInputAction = (event) => {
        if($scope.chatInputValue && $scope.chatInputValue.length > 0) {
            let payload = JSON.stringify({
                "data" : $scope.chatInputValue,
                "timestamp" : (new Date()).getTime()
            });

            $http.post("http://localhost:8000/chatify", payload).then((response) => {
                $scope.chatInputValue = "";
                if(event) {
                    event.preventDefault();
                }
            }, (response) => {
                console.error(response.data);
            });
        }
    };

    document.addEventListener("keypress", (event) => {
        let key = event.which || event.keyCode;

        if(key === 13 && $scope.chatInputFocus) {
            $scope.chatInputAction();
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