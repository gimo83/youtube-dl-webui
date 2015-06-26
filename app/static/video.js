$(document).ready(function(){

   var div_container = $('#container');
   var req_videos = $.ajax({url: "/api/service/videos"});
   req_videos.done(function(data){
       var div_container = $('#container');
       for( var video_index in data.result){
	   console.log(data.result[video_index])
	   var video_id = data.result[video_index].id;
	   var _id = data.result[video_index]._id;
	   //set video image
	   var video_image ="";
	   if(data.result[video_index].extractor_key == 'Youtube'){
	       video_image  = "<img src='"+ data.result[video_index].thumbnail+"' class='img-responsive' alt='Mountain View' width='140px' height='100px' >";
	   }
	   else{
	       video_image  = "<img src='"+ data.result[video_index].entries[0].thumbnail +"' class='img-responsive' alt='Mountain View' width='140px' height='100px'>"
                              + "<div class='pull-right' style='background:black'></div>";
	   }
	   //set progragebar
	   var video_progress = "<div></div>";
	   if('dl_status' in data.result[video_index]){
	       var barStatus = (data.result[video_index].dl_status.status == 'downloading')?'active':'';
	       var barValue  = (data.result[video_index].dl_status.status == 'downloading')?data.result[video_index].dl_status.downloaded_bytes : 100;
	       var barMaxVal = (data.result[video_index].dl_status.status == 'finshed')?data.result[video_index].dl_status.total_bytes:100;
	       var barWidth  = (data.result[video_index].dl_status.status == 'downloading')?data.result[video_index].dl_status._percent_str:'100%';
	       var innerText = (data.result[video_index].dl_status.status == 'downloading')?data.result[video_index].dl_status._percent_str:'100%';
	       video_progress = "<div class='progress-bar progress-bar-success progress-bar-striped"+ barStatus +"'"
		                +" role='progressbar' aria-valuenow='"+ barValue +"' "
                                +" aria-valuemin='0' aria-valuemax='"+ barMaxVal  +"' "
		                +" style='width:"+ barWidth +"'>"
                                   +innerText +"</div>"  
	   }




	    $('#container').append(
		"<div id='"+_id+"' class='row thumbnail' style='margin-bottom: 7px;'>"
		    +"<div class='col-xs-2'>"+ video_image +"</div>"
		    +"<div class='col-xs-offset-2 row'>"
		       +"<p>"+ data.result[video_index].title +"</p>"
                       +"<div class='progress' style='width:95%;margin-bottom:5px'>"
                           + video_progress
                       +"</div>"
                       +"<p><a href='video/download/"+_id+"'><span class='glyphicon glyphicon-cloud-download'></span></a> &nbsp;"
                       +"<a href='video/delete/"+_id+"'><sapn class='glyphicon glyphicon-trash'></span></a></p>"
                    +"</div>"
                    +"</div>"
	    );
	   }
   });
});
