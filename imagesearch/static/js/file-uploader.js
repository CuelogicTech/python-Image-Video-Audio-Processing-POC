var myApp = angular.module('myApp', []);

myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
        
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);


myApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fileData = new FormData();
        fileData.append('file', file)
      
        $http.post(uploadUrl, fileData, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
  
        .success(function(msg){
            // alert(msg);
            if (msg['filename']){
                window.location = "/core/search/"+"?f="+msg['filename'];
            }
            else{
                alert('Upload a file to proceed with search')
            }
            return false;
        })
        .error(function(msg){
            alert(msg);
        });
    }
}]);

myApp.service('bankUpload', ['$http', function ($http) {
    this.uploadFileToBank = function(file, uploadUrl){
        var fileData = new FormData();
        fileData.append('file', file)
      
        $http.post(uploadUrl, fileData, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
  
        .success(function(msg){
            // alert(msg);
            if (msg['success']){
                alert('File Uploaded');
            }
            else{
                alert(msg['error']);
            }
            return false;
        })
        .error(function(msg){
            alert(msg);
        });
    }
}]);

myApp.controller('myCtrl', ['$scope', 'fileUpload', 'bankUpload', function($scope, fileUpload, bankUpload){
    $scope.uploadFile = function(){
        var file = $scope.myFile;
        console.log(file);
        var uploadUrl = "core/fileupload/upload-file/";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
    $scope.uploadBank = function(){
        var file = $scope.myFile;
        console.log(file);
        var uploadUrl = "core/fileupload/upload-file-bank/";
        bankUpload.uploadFileToBank(file, uploadUrl);
    };
}]);