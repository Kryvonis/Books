angular.module('books', [])
    .controller('BooksSearchController', ['$scope', '$http', '$location', '$window',
        function ($scope, $http, $location, $window) {
            $scope.startSearch = function (searchText, emailText) {
                var data = JSON.stringify({'searchText': searchText, email: emailText});
                $http.post('/search', data).success(function (data, status, headers, config) {
                    // this callback will be called asynchronously
                    // when the response is available
                    $window.location.href = '/result'
                    
                }).error(function (data, status, headers, config) {
                    $window.location.href = '/err'
                });
            };
        }
    ]);