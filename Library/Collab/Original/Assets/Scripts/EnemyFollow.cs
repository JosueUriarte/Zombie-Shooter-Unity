using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;
using UnityEngine.AI;
//using TextToGraph.TextToMap;

public class EnemyFollow : MonoBehaviour
{
	public TextMapping[] mappingData;
	public TextAsset mapText;
    public Rigidbody2D rb;
    public float speed;
    public Transform target;
	public  TextToGraph TTG;
	//x position y position and distance value
	List<(float, float)> xy = TTG.GenerateGraph(mappingData, mapText);
	
	
    // Start is called before the first frame update
    void Start()
    {
        rb = this.GetComponent<Rigidbody2D>();
        target = GameObject.FindGameObjectWithTag("Player").GetComponent<Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 direction = target.position - transform.position;
        float angle = Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg;
        rb.rotation = angle;
		
        if (Vector2.Distance(transform.position, target.position) > 0)
        {
            transform.position = Vector2.MoveTowards(transform.position, target.position, speed * Time.deltaTime);
        }


    }
    void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.tag == "Player")
        {
            Destroy(collision.gameObject);
        }
    }

	/*void Astar(List<(float, float)> Graph, List<(float, float)> weights) 
	{

	}*/

	
	
}
