let account = angular.module('account', [], ($interpolateProvider) => {
     $interpolateProvider.startSymbol('[[');
     $interpolateProvider.endSymbol(']]');
});

account.controller('settings', ['$scope', '$http', ($scope, $http) => {
    $scope.state = {
        edit : false,
        persistence : false,
        focus : false,
        message : null
    };

    $scope.focusImgEdit = () => {
        $scope.state.focus = true;
    };

    $scope.blurImgEdit = () => {
        $scope.state.focus = false;
    };

    let file = null;
    $scope.uploadFile = (files) => {
        file = files[0];

        let fileReader = new FileReader();
        fileReader.onload = function() {
            let profile = document.querySelector(".picture-placeholder");
            profile.src = fileReader.result;

            $scope.state.edit = true;
            $scope.state.message = "Edit Mode";
            $scope.$apply();
        };

        fileReader.readAsDataURL(files[0]);
    };

    $scope.applyChanges = () => {
        if(!file) {
            return;
        }

        let data = new FormData();
        data.append("file", file);

        $http.post("http://localhost:8000/account", data, {
            withCredentials: true,
            headers: {'Content-Type': undefined },
            transformRequest: angular.identity
        }).then((_) => {
            $scope.state.message = "Saved";
            $scope.state.persistence = true;
            $scope.state.edit = false;
        }, (response) => {
            $scope.state.message = response.data;
        });
    };

    $scope.uploadTriggerFile = () => {
        setTimeout(function() {
            document.querySelector('.picture-upload').click();
        }, 0);
    };
}]);