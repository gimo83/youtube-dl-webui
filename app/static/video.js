var updateDataTimer;

function addVideo(video){
   //set video image                                                                                                                                                                                
   var video_image ="";
   if(video.extractor_key == 'Youtube'){
       video_image  = "<img src='"+ video.thumbnail+"' class='img-responsive' alt='Mountain View' width='140px' height='100px' >";
   }
   else{
       video_image  = "<img src='"+ video.entries[0].thumbnail +"' class='img-responsive' alt='Mountain View' width='140px' height='100px'>"
                      + "<div class='pull-right' style='background:black'></div>";
   }
   //set progragebar                                                                                                                                                                                
   var video_progress = "<div class='progress-bar progress-bar-success progress-bar-striped' role='progressbar' aria-valuenow='0' aria-valuemin='0' aria-valuemax='100' style='width:0'></div>";
   if('dl_status' in video){
       var barStatus = (video.dl_status.status == 'downloading')?'active':'';
       var barValue  = (video.dl_status.status == 'downloading')?video.dl_status.downloaded_bytes : 100;
       var barMaxVal = (video.dl_status.status == 'finshed')?video.dl_status.total_bytes:100;
       var barWidth  = (video.dl_status.status == 'downloading')?video.dl_status._percent_str:'100%';
       var innerText = (video.dl_status.status == 'downloading')?video.dl_status._percent_str:'100%';
       video_progress = "<div class='progress-bar progress-bar-success progress-bar-striped "+ barStatus +"'"
                        +" role='progressbar' aria-valuenow='"+ barValue +"' "
                        +" aria-valuemin='0' aria-valuemax='"+ barMaxVal  +"' "
                        +" style='width:"+ barWidth +"'>"
                           +innerText +"</div>"
   }

    $('#container').append(
        "<div id='"+video._id+"' class='row thumbnail' style='margin-bottom: 7px;'>"
            +"<div class='col-xs-2'>"+ video_image +"</div>"
            +"<div class='col-xs-offset-2 row'>"
               +"<p>"+ video.title +"</p>"
               +"<div class='progress' style='width:95%;margin-bottom:5px'>"
                   + video_progress
               +"</div>"
               +"<p><a  onclick='downloadVideo(this)'><span class='glyphicon glyphicon-cloud-download'></span></a> &nbsp;"
               +"<a onclick='deleteVideo(this)'><sapn class='glyphicon glyphicon-trash'></span></a></p>"
            +"</div>"
            +"</div>"
    );
}


function updateVideo(video){
    if('dl_status' in video){
	console.log(video.dl_status);
	var tag_id_class = "#"+video._id+" .progress-bar";
	var progBar = $(tag_id_class);
	var barStatus = "progress-bar progress-bar-success progress-bar-striped ";
	//make progress bar active
	if(video.dl_status.status == 'downloading')
	    barStatus +=  "active";

        var barValue  = (video.dl_status.status == 'downloading')?video.dl_status.downloaded_bytes : 100;
        var barMaxVal = (video.dl_status.status == 'finshed')?video.dl_status.total_bytes:100;
        var barWidth  = (video.dl_status.status == 'downloading')?video.dl_status._percent_str:'100%';
        var innerText = (video.dl_status.status == 'downloading')?video.dl_status._percent_str:'100%';
	
	//make progress bar acttive
	progBar.attr('class',barStatus);
	progBar.attr('aria-valuenow',barValue);
	progBar.attr('aria-valuemax',barMaxVal);
	progBar.width(barWidth);
	progBar.html(innerText);
    }
}

function removeVideo(id){
  var tag_id = "#"+id;
  $(tag_id).remove();
}

function processDeleteVideo(data){
  if (data.result.status == "ok") {
    removeVideo(data.result._id);
  };
}

function deleteVideo(caller){
  var id = $(caller).parent().parent().parent().attr('id');
  var video_url = "/api/service/videos/"+id; 
  $.ajax({url:video_url,method:'DELETE',success:processDeleteVideo})
}


function processDownloadVideo(data){
  if (data.result.status == "ok") {
    //updateVideo(data.result._id);
  };
}

function downloadVideo(caller){
  var id = $(caller).parent().parent().parent().attr('id');
  var video_url = "/api/service/download/"+id; 
  $.ajax({url:video_url})
}


function processVideoList(videoList){
  for( var video_index in videoList.result){
      var tag_id = "#"+videoList.result[video_index]._id;
      
      if($(tag_id).length != 0){
        updateVideo(videoList.result[video_index]);
      }
      else{
        addVideo(videoList.result[video_index]);
      }
  }

  updateDataTimer = setTimeout(loadVideolist,2000);
}

function loadVideolist(){
   var req_videos = $.ajax({url: "/api/service/videos",success:processVideoList});
}

$(document).ready(loadVideolist);
