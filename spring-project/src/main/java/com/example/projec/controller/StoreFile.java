package com.example.projec.controller;


import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;

@RestController
@RequestMapping("/store")
public class StoreFile {
    @RequestMapping("/storefile")
    public String storeFile(@RequestPart("files[]") MultipartFile[] files) {
        for (MultipartFile file : files) {
            System.out.println(file.getOriginalFilename());
            try {
                file.transferTo(new File("E:/vue-data/" + file.getOriginalFilename()));
            } catch (IOException e) {
                e.printStackTrace();
                return "Failed to store " + file.getOriginalFilename();
            }
        }
        return "success";
    }
}
