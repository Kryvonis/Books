angular.module('books', [])
    .controller('BooksSearchController', ['$scope', '$http', '$location', '$window',
        function ($scope, $http, $location, $window) {
            $scope.startSearch = function (searchText, emailText) {
                var data = JSON.stringify({'searchText': searchText, email: emailText});
                $http.post('/search', data).success(function (data, status, headers, config) {
                    // this callback will be called asynchronously
                    // when the response is available
                    $window.location.href = '/result'
                    // $location.path('/result');
                    // $location.replace();

                }).error(function (data, status, headers, config) {
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                    $window.location.href = '/err'
                });

                // $http.get('/result',data).success(function ( status, headers, config) {
                //     // this callback will be called asynchronously
                //     // when the response is available
                // }).error(function (status, headers, config) {
                //     // called asynchronously if an error occurs
                //     // or server returns response with an error status.
                // });
            };

        }]);