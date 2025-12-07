"""
Database utilities for Mind Palace MongoDB operations.
"""
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['mind_palace']
        self.notebooks = self.db['notebooks']
        self.progress = self.db['progress']
        
    def save_notebook(self, filename, pdf_content, text_content, summary, topics):
        """Save a new notebook to the database."""
        notebook = {
            'filename': filename,
            'pdf_content': pdf_content,
            'text_content': text_content,
            'summary': summary,
            'topics': topics,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = self.notebooks.insert_one(notebook)
        return str(result.inserted_id)
    
    def get_notebook(self, notebook_id):
        """Retrieve a notebook by ID."""
        from bson.objectid import ObjectId
        return self.notebooks.find_one({'_id': ObjectId(notebook_id)})
    
    def get_all_notebooks(self):
        """Get all notebooks."""
        return list(self.notebooks.find().sort('created_at', -1))
    
    def update_notebook(self, notebook_id, update_data):
        """Update notebook data."""
        from bson.objectid import ObjectId
        update_data['updated_at'] = datetime.now()
        return self.notebooks.update_one(
            {'_id': ObjectId(notebook_id)},
            {'$set': update_data}
        )
    
    def save_schedule(self, notebook_id, schedule, days):
        """Save study schedule for a notebook."""
        self.update_notebook(notebook_id, {
            'schedule': schedule,
            'schedule_days': days
        })
    
    def get_progress(self, notebook_id):
        """Get progress for a notebook."""
        from bson.objectid import ObjectId
        progress = self.progress.find_one({'notebook_id': notebook_id})
        if not progress:
            # Initialize progress
            progress = {
                'notebook_id': notebook_id,
                'completed_tasks': [],
                'total_score': 0,
                'created_at': datetime.now()
            }
            self.progress.insert_one(progress)
        return progress
    
    def mark_task_complete(self, notebook_id, day, task_index, points):
        """Mark a task as completed and add points."""
        from bson.objectid import ObjectId
        task_id = f"{day}_{task_index}"
        
        progress = self.get_progress(notebook_id)
        
        if task_id not in progress.get('completed_tasks', []):
            self.progress.update_one(
                {'notebook_id': notebook_id},
                {
                    '$push': {'completed_tasks': task_id},
                    '$inc': {'total_score': points},
                    '$set': {'updated_at': datetime.now()}
                }
            )
            return True
        return False
    
    def delete_notebook(self, notebook_id):
        """Delete a notebook and its progress."""
        from bson.objectid import ObjectId
        self.notebooks.delete_one({'_id': ObjectId(notebook_id)})
        self.progress.delete_many({'notebook_id': notebook_id})
