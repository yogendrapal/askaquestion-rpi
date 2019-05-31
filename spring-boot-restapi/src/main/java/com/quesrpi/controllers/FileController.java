package com.quesrpi.controllers;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
//import java.util.Arrays;
//import java.util.List;
//import java.util.stream.Collectors;

import com.quesrpi.payload.UploadFileResponse;
import com.quesrpi.service.FileStorageService;

@ComponentScan({"com.quesrpi.service"})
@RestController
public class FileController {
	private static final Logger logger = LoggerFactory.getLogger(FileController.class);

	
	@Autowired
    private FileStorageService fileStorageService;
	
	@PostMapping("/question/add/{qid}")
    public UploadFileResponse uploadFile(@PathVariable String qid, @RequestParam("file") MultipartFile file) {
        String fileName = fileStorageService.storeFile(file,qid);

        String fileDownloadUri = ServletUriComponentsBuilder.fromCurrentContextPath()
                .path("/question/")
                .path(qid)
                .toUriString();

        return new UploadFileResponse(fileName, fileDownloadUri,
                file.getContentType(), file.getSize());
    }
	
	@GetMapping("/question/{qid}")//downloadFile/{fileName:.+}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String qid, HttpServletRequest request) {
        // Load file as Resource
        Resource resource = fileStorageService.loadFileAsResource(qid+".mp4");

        // Try to determine file's content type
        String contentType = null;
        try {
            contentType = request.getServletContext().getMimeType(resource.getFile().getAbsolutePath());
        } catch (IOException ex) {
            logger.info("Could not determine file type.");
        }

        // Fallback to the default content type if type could not be determined
        if(contentType == null) {
            contentType = "application/octet-stream";
        }

        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(contentType))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + resource.getFilename() + "\"")
                .body(resource);
    }
}
