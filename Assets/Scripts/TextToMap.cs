using UnityEngine;
using System.Text.RegularExpressions;
using System.Collections.Generic;

public class TextToMap : MonoBehaviour
{
	public TextMapping[] mappingData;
	public TextAsset mapText;
	//public TextMapping[] zombieSpawn;
	//private List<(float, float)> xy = new List<(float, float)>();
	
	private Vector2 currentPosition = new Vector2(0, 0);
	
    // Start is called before the first frame update
    void Start()
    {
		GenerateMap();
		//InvokeRepeating("Spawner", 0f, 5f);
    }
	
	void Spawner()
	{
		/** Vector2 currentPositionR = new Vector2(0, 0);
		string[] rows = Regex.Split(mapText.text, "\r\n|\r|\n");
		foreach(string row in rows) 
		{
			foreach(char c in row) 
			{
				foreach(TextMapping tm in zombieSpawn) 
				{
					if (c == tm.character) 
					{
						Instantiate(tm.prefab, currentPositionR, Quaternion.identity, transform);
					}
				}
				currentPositionR = new Vector2(++currentPositionR.x, currentPositionR.y);
			}
			currentPositionR = new Vector2(0, ++currentPositionR.y);
		}
		**/
	}
	
	private void GenerateMap() 
	{
		string[] rows = Regex.Split(mapText.text, "\r\n|\r|\n");
		foreach(string row in rows) 
		{
			foreach(char c in row) 
			{
				foreach(TextMapping tm in mappingData) 
				{
					if (c == tm.character) 
					{
						Instantiate(tm.prefab, currentPosition, Quaternion.identity, transform);
					}
				}
				currentPosition = new Vector2(++currentPosition.x, currentPosition.y);
			}
			currentPosition = new Vector2(0, ++currentPosition.y);
		}
	}
}
