#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <unistd.h>
#include <errno.h>

#define MAXSIZE 256
#include <iostream>
//using namespace std;


int main(int argc, char** argv)
{
	DIR* FD;
	DIR* FD_SUB;
	DIR* FD_SUB_SUB;
	struct dirent* root_dir;
	struct dirent* action_types_dir;
	struct dirent* action_frames_dir;
	struct dirent* current_file_ent;
	const char* previous_file=NULL;
	const char* current_file;
	
	const char* root_path = "/home/wangyf/data/ucf101_frm/";
	/*Open Root directory of data*/
	if (NULL==(FD = opendir(root_path)))
	{
		fprintf(stderr, "Error: Failed to open input directory - %s\n", strerror(errno));
		return 1;
	}
	while((action_types_dir= readdir(FD)))
	{
		if (!strcmp(action_types_dir->d_name, ".") || !strcmp(action_types_dir->d_name, ".."))
		{
			continue;
		}	
		
		/*Read sub directory*/
		const char* action_types_dir_name = action_types_dir->d_name;
		char sub_path[MAXSIZE];
		strcpy(sub_path, root_path);
		strcat(sub_path, action_types_dir_name);
		const char* sub_path_const = sub_path;
		printf("action type directory: %s\n", sub_path_const);
		if (NULL == (FD_SUB=opendir(sub_path_const)))
		{
			fprintf(stderr, "Error: Failed to open input directory - %s\n", strerror(errno));
			return 1;
		}
		
		/*Read the directory contains frames*/
		while((action_frames_dir = readdir(FD_SUB)))
		{
			if (!strcmp(action_frames_dir->d_name, ".") || !strcmp(action_frames_dir->d_name, ".."))
			{
				continue;
			}	
			
			const char* frames_dir_name = action_frames_dir->d_name;
			
			char frames_path[MAXSIZE];
			strcpy(frames_path, sub_path_const);
			strcat(frames_path, "/");
			strcat(frames_path, frames_dir_name);
			printf("Frames' path: %s\n", frames_path);
			const char* frames_path_const = frames_path;
			
			/*Read the name of every two frames*/
			if ((NULL == (FD_SUB_SUB=opendir(frames_path_const))))
			{
				fprintf(stderr, "Error: Failed to open input directory - %s\n", strerror(errno));
				return 1;
			}
			
			while((current_file_ent = readdir(FD_SUB_SUB)))
			{
				if (!strcmp(current_file_ent->d_name, ".") || !strcmp(current_file_ent->d_name, ".."))
				{
					continue;
				}	
				
				current_file = current_file_ent->d_name;
				if (previous_file == NULL)
				{
					previous_file = current_file;
				}
				//call the function doing main the job
				printf("previouse file:%s\n current file:%s\n", previous_file, current_file);

				previous_file = current_file;
				
			}
	
		}	
		
	}
	
	return 0;
}
