package uavnetwork;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;

import javax.vecmath.Point3d;

import javafx.scene.shape.Circle;

import uavnetwork.NeighbourProperties;
import uavnetwork.Packet;

public class Uav
{
	private int uavId;
	private Point3d center;
	private int radius;
	private Circle area ;
	private Map<Integer, Queue<Packet>> tranQueue;
	private Map<Integer, Queue<Packet>> recQueue;
	
	private List<Uav> neighbours;
	private int threshold;
	private Map<Integer, NeighbourProperties> nProp;
	
	private boolean positionChanged;

	public Uav(int uavId, Point3d center, int radius, int threshold)
	{
		
		this.uavId = uavId;
		this.center = center;
		this.radius = radius;
		this.threshold = threshold;
		this.tranQueue = new HashMap<Integer, Queue<Packet>>();
		this.recQueue = new HashMap<Integer, Queue<Packet>>();
		this.neighbours = new ArrayList<Uav>();
		this.nProp = new HashMap<Integer, NeighbourProperties>();
		this.positionChanged = false;
		
	}
	
	
	
	public boolean isPositionChanged()
	{
		return positionChanged;
	}



	public void setPositionChanged(boolean positionChanged)
	{
		this.positionChanged = positionChanged;
	}



	public void changeCoordinates(Point3d newCenter)
	{
		this.center = newCenter;
	}
	
	public void addTransQueue(Integer uavId, Packet p)
	{
		Queue<Packet> queue = this.tranQueue.get(uavId);
		queue.add(p);
	}
	
	public void remTransQueue(Integer uavId)
	{
		Queue<Packet> queue = this.tranQueue.get(uavId);
		queue.poll();
	}
	
	public void addRecvQueue(Integer uavId, Packet p)
	{
		Queue<Packet> queue = this.recQueue.get(uavId);
		queue.add(p);
	}
	
	public void remRecvQueue(Integer uavId)
	{
		Queue<Packet> queue = this.recQueue.get(uavId);
		queue.poll();
	}
	
	public void setUavId(int uavId)
	{
		this.uavId = uavId;
	}
	
	public int getUavId()
	{
		return uavId;
	}

	
	public Point3d getCenter()
	{
		return center;
	}
	public void setCenter(Point3d center)
	{
		this.center = center;
	}
	public int getRadius()
	{
		return radius;
	}
	public void setRadius(int radius)
	{
		this.radius = radius;
	}
	public Circle getArea()
	{
		return area;
	}
	public void setArea(Circle area)
	{
		this.area = area;
	}
	public void setTranQueue(Map<Integer, Queue<Packet>> tranQueue)
	{
		this.tranQueue = tranQueue;
	}

	public void setRecQueue(Map<Integer, Queue<Packet>> recQueue)
	{
		this.recQueue = recQueue;
	}
	
	
	
	public Map<Integer, Queue<Packet>> getTranQueue()
	{
		return tranQueue;
	}

	public Map<Integer, Queue<Packet>> getRecQueue()
	{
		return recQueue;
	}

	public List<Uav> getNeighbours()
	{
		return neighbours;
	}
	public void setNeighbours(List<Uav> neighbours)
	{
		this.neighbours = neighbours;
	}
	public int getThreshold()
	{
		return threshold;
	}
	public void setThreshold(int threshold)
	{
		this.threshold = threshold;
	}
	public Map<Integer, NeighbourProperties> getnProp()
	{
		return nProp;
	}
	public void setnProp(Map<Integer, NeighbourProperties> nProp)
	{
		this.nProp = nProp;
	}
	
	
	
}
