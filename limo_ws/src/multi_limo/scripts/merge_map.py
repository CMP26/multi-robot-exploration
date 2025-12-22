#!/usr/bin/env python3
# Fixed version for gmapping compatibility - Frame ID corrected

import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np

def merge_maps(map1, map2):
    """Merge two OccupancyGrid maps into a single merged map."""
    merged_map = OccupancyGrid()
    merged_map.header = map1.header
    
    # CRITICAL FIX: Use 'map' frame (gmapping standard)
    merged_map.header.frame_id = map1.header.frame_id  # Preserve original frame
    
    # Validate resolution compatibility
    if abs(map1.info.resolution - map2.info.resolution) > 0.001:
        rospy.logwarn(f"Resolution mismatch: map1={map1.info.resolution}, map2={map2.info.resolution}")
        resolution = map1.info.resolution
    else:
        resolution = map1.info.resolution
    
    # Calculate the bounding box of both maps
    min_x = min(map1.info.origin.position.x, map2.info.origin.position.x)
    min_y = min(map1.info.origin.position.y, map2.info.origin.position.y)
    max_x = max(map1.info.origin.position.x + (map1.info.width * map1.info.resolution),
                map2.info.origin.position.x + (map2.info.width * map2.info.resolution))
    max_y = max(map1.info.origin.position.y + (map1.info.height * map1.info.resolution),
                map2.info.origin.position.y + (map2.info.height * map2.info.resolution))
    
    # Set merged map properties
    merged_map.info.origin.position.x = min_x
    merged_map.info.origin.position.y = min_y
    merged_map.info.origin.position.z = 0.0
    merged_map.info.origin.orientation.w = 1.0
    merged_map.info.resolution = resolution
    merged_map.info.width = int(np.ceil((max_x - min_x) / resolution))
    merged_map.info.height = int(np.ceil((max_y - min_y) / resolution))
    
    # Initialize merged map with unknown values (-1)
    merged_map.data = [-1] * (merged_map.info.width * merged_map.info.height)
    
    def copy_map_data(source_map, merged_map):
        for y in range(source_map.info.height):
            for x in range(source_map.info.width):
                i = x + y * source_map.info.width
                
                # Calculate world coordinates (center of cell)
                world_x = source_map.info.origin.position.x + (x + 0.5) * source_map.info.resolution
                world_y = source_map.info.origin.position.y + (y + 0.5) * source_map.info.resolution
                
                # Transform to merged map coordinates
                merged_x = int((world_x - merged_map.info.origin.position.x) / merged_map.info.resolution)
                merged_y = int((world_y - merged_map.info.origin.position.y) / merged_map.info.resolution)
                
                # Bounds checking
                if 0 <= merged_x < merged_map.info.width and 0 <= merged_y < merged_map.info.height:
                    merged_i = merged_x + merged_y * merged_map.info.width
                    if 0 <= i < len(source_map.data):
                        # Only overwrite if current cell is unknown
                        if merged_map.data[merged_i] == -1:
                            merged_map.data[merged_i] = source_map.data[i]
    
    # Copy both maps
    copy_map_data(map1, merged_map)
    copy_map_data(map2, merged_map)
    
    return merged_map


def merge_multiple_maps(maps):
    """Merge multiple maps sequentially."""
    if len(maps) == 0:
        return None
    if len(maps) == 1:
        return maps[0]
    
    merged = merge_maps(maps[0], maps[1])
    
    for i in range(2, len(maps)):
        merged = merge_maps(merged, maps[i])
    
    return merged


class MergeMapNode:
    def __init__(self):
        rospy.init_node('merge_map_node')
        
        # Get parameters
        self.map_topics = rospy.get_param('~map_topics', ['/map1', '/map2'])
        self.merged_topic = rospy.get_param('~merged_topic', '/merged_map')
        self.merge_rate = rospy.get_param('~merge_rate', 1.0)
        
        rospy.loginfo(f"Map Merger Node initialized")
        rospy.loginfo(f"Subscribing to topics: {self.map_topics}")
        rospy.loginfo(f"Publishing merged map to: {self.merged_topic}")
        
        self.publisher = rospy.Publisher(self.merged_topic, OccupancyGrid, queue_size=10)
        
        self.maps = {}
        self.last_map_time = {}
        
        self.subscribers = []
        for topic in self.map_topics:
            sub = rospy.Subscriber(topic, OccupancyGrid, self.map_callback, callback_args=topic)
            self.subscribers.append(sub)
        
        self.timer = rospy.Timer(rospy.Duration(1.0 / self.merge_rate), self.merge_and_publish)
        
        rospy.loginfo("Map Merger Node ready")
    
    def map_callback(self, msg, topic):
        """Callback function for map messages."""
        # Validate map data
        if msg.info.width <= 0 or msg.info.height <= 0:
            rospy.logwarn(f"Invalid map dimensions from {topic}")
            return
        
        if len(msg.data) != msg.info.width * msg.info.height:
            rospy.logwarn(f"Map data size mismatch from {topic}")
            return
        
        self.maps[topic] = msg
        self.last_map_time[topic] = rospy.Time.now()
        rospy.logdebug(f"Received map from {topic}: {msg.info.width}x{msg.info.height}, frame: {msg.header.frame_id}")
    
    def merge_and_publish(self, event):
        """Merge all available maps and publish the result."""
        if len(self.maps) < 1:
            return
        
        # Remove stale maps (optional timeout)
        timeout = rospy.Duration(10.0)
        current_time = rospy.Time.now()
        stale_topics = [topic for topic, last_time in self.last_map_time.items() 
                       if current_time - last_time > timeout]
        for topic in stale_topics:
            rospy.logwarn(f"Removing stale map: {topic}")
            del self.maps[topic]
            del self.last_map_time[topic]
        
        available_maps = list(self.maps.values())
        
        if len(available_maps) == 0:
            return
        
        if len(available_maps) == 1:
            merged_map = available_maps[0]
            merged_map.header.stamp = rospy.Time.now()
        else:
            merged_map = merge_multiple_maps(available_maps)
            if merged_map is not None:
                merged_map.header.stamp = rospy.Time.now()
        
        if merged_map is not None:
            self.publisher.publish(merged_map)
            rospy.logdebug(f"Published merged map: {merged_map.info.width}x{merged_map.info.height}, frame: {merged_map.header.frame_id}")
    
    def run(self):
        """Keep the node running."""
        rospy.spin()


def main():
    try:
        node = MergeMapNode()
        node.run()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()