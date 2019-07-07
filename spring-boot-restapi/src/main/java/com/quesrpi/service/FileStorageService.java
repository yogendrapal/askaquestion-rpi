package com.quesrpi.service;


import com.quesrpi.beans.Question;
import com.quesrpi.exception.FileStorageException;
import com.quesrpi.exception.MyFileNotFoundException;

import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.configurationprocessor.json.JSONObject;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import com.quesrpi.property.FileStorageProperties;

import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

@Service
public class FileStorageService {

	private final Path fileStorageLocation;
	private final Path answerStorageLocation;
	
	@Autowired
	private QuestionRepository repository;
	
	@Autowired
    public FileStorageService(FileStorageProperties fileStorageProperties) {
        this.fileStorageLocation = Paths.get(fileStorageProperties.getUploadDir())
                .toAbsolutePath().normalize();
        this.answerStorageLocation = Paths.get(fileStorageProperties.getAnswerDir())
                .toAbsolutePath().normalize();
        
        try {
            Files.createDirectories(this.fileStorageLocation);
        } catch (Exception ex) {
            throw new FileStorageException("Could not create the directory where the uploaded files will be stored.", ex);
        }
    }
	/*
	 * This function is used to send the video with relevant details to 
	 * the app server for processing.
	 */
	public void sendVideo(String filename, Question q) {
		
		String serverUrl = "http://104.237.9.77:50000/uploadDeviceQuestion";
		
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.MULTIPART_FORM_DATA);
		MultiValueMap<String, Object> body
		  = new LinkedMultiValueMap<>();
		Process p;
		if(filename.endsWith("avi")) {
			/*
			 * THE FILE NEEDS TO BE CONVERTED TO .MP4 AS THE ANDROID PLAYER
			 * IS NOT SUPPORTING .AVI
			 * This needs to be improved in the future
			 */
			String orig_path = this.fileStorageLocation.resolve(filename).toString();
//			System.out.println(orig_path);
			String dest_name = filename.substring(0,filename.lastIndexOf(".")) + ".mp4";
			String dest_path = this.fileStorageLocation.resolve(dest_name).toString();
//			System.out.println(dest_path);
			String convcommand = "ffmpeg -y -i " + orig_path + " -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 " + dest_path;
			System.out.println(convcommand);
			try {
				p = Runtime.getRuntime().exec(convcommand);
				p.waitFor();
				System.out.println ("ffmpeg exit: " + p.exitValue());
	            p.destroy();
				filename = dest_name;
			}
			catch(Exception econv) {
				System.out.println(econv.toString());
			}
		}
		
		Resource vidResource = loadFileAsResource(filename,'q');
		
		body.add("file", vidResource);
		body.add("deviceId", q.getMachine_id());
		body.add("videoId", q.get_id());
		body.add("instituteId", q.getInstituteId());
		
		HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
		 
		 
		RestTemplate restTemplate = new RestTemplate();
		ResponseEntity<String> response  = restTemplate.postForEntity(serverUrl, requestEntity, String.class);
		String responseBody = response.getBody();
		System.out.println(responseBody);
	}
	
	public String storeFile(MultipartFile file,String newFileName, char type) {
        // Normalize file name
        String fileName = StringUtils.cleanPath(file.getOriginalFilename());
//        System.out.println(fileName);
        int lastIndex = fileName.lastIndexOf(".");
        if(lastIndex == -1) {
        	fileName = newFileName;
        }
        else {
        	fileName = newFileName+fileName.substring(lastIndex);
        }
        //newFileName contains the qid, so, we use it to find the record
        Question record = repository.findBy_id(new ObjectId(newFileName));
        if(record == null) {
        	return null;
        }
        try {
            // Check if the file's name contains invalid characters
            if(fileName.contains("..")) {
                throw new FileStorageException("Sorry! Filename contains invalid path sequence " + fileName);
            }

            // Copy file to the target location (Replacing existing file with the same name)
            Path targetLocation;
            if(type == 'q')
            	targetLocation = this.fileStorageLocation.resolve(fileName);
            else
            	targetLocation = this.answerStorageLocation.resolve(fileName);
            Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);
            try {
//            	if(type == 'q')
//            		sendVideo(fileName, record);
            }
            catch(Exception senderr) {
            	System.out.println(senderr.toString());
            	System.out.println("Difficulty communicating with other server!");
            }
            
            return fileName;
        } catch (IOException ex) {
            throw new FileStorageException("Could not store file " + fileName + ". Please try again!", ex);
        }
    }
	
	 public Resource loadFileAsResource(String fileName, char type) {
	        try {
	        	Path filePath;
	        	Resource resource;
	        	if(type == 'q') {
	        		filePath = this.fileStorageLocation.resolve(fileName).normalize();
	        		resource = new UrlResource(filePath.toUri());
	        	}	
	            else {
	            	/*
	            	 * THIS IS A TEMPORARY SOLUTION, THIS NEEDS TO BE CHANGED!
	            	 */
	            	filePath = this.answerStorageLocation.resolve(fileName+".mp4").normalize();
	            	resource = new UrlResource(filePath.toUri());
	            	if(!resource.exists()) {
	            		filePath = this.answerStorageLocation.resolve(fileName+".avi").normalize();
	            	}
	            	resource = new UrlResource(filePath.toUri());
	            }
	            if(resource.exists()) {
	                return resource;
	            } else {
	                throw new MyFileNotFoundException("File not found " + fileName);
	            }
	        } catch (MalformedURLException ex) {
	            throw new MyFileNotFoundException("File not found " + fileName, ex);
	            
	        }
	    }
	
}
